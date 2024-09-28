from datetime import date
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from models.endereco_model import Endereco
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import NOME_COOKIE_AUTH, criar_token, obter_hash_senha

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_root(request: Request):
    usuario = request.state.usuario if hasattr(request.state, "usuario") else None
    if not usuario:
        return templates.TemplateResponse("pages/entrar.html", {"request": request})
    if usuario.perfil == 1:
        return RedirectResponse("/cliente", status_code=status.HTTP_303_SEE_OTHER)
    if usuario.perfil == 2:
        return RedirectResponse("/vendedor", status_code=status.HTTP_303_SEE_OTHER)
@router.post("/post_entrar")
async def post_entrar(
    email: str = Form(...), 
    senha: str = Form(...)):
    usuario = UsuarioRepo.checar_credenciais(email, senha)
    print(f"Usuário encontrado: {usuario}")  # Adicione um log aqui
    if usuario is None:
        print("Credenciais inválidas")  # Log para falha
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    

    token = criar_token(usuario[0], usuario[1], usuario[2])
    nome_perfil = None
    match (usuario[2]):
        case 1: nome_perfil = "cliente"
        case 2: nome_perfil = "vendedor"
        case _: nome_perfil = ""
    
    response = RedirectResponse(f"/{nome_perfil}", status_code=status.HTTP_303_SEE_OTHER)    
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value=token,
        max_age=3600*24*365*10,
        httponly=True,
        samesite="lax"
    )
    return response

@router.get("/cadastrar")
async def get_cadastrar(request: Request):
    return templates.TemplateResponse("pages/cadastrar.html", {"request": request})

@router.post("/post_cadastrar")
async def post_cadastrar(
    nome: str = Form(...),
    sobrenome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    senha: str = Form(...),
    confsenha: str = Form(...),
    perfil: int = Form(...),
    cep: str = Form(...),
    numero: str = Form(...),
    complemento: str = Form(),
    endereco: str = Form(...),
    cidade: str = Form(...),
    uf: str = Form(...)
    ):
    if senha != confsenha:
        return RedirectResponse("/cadastrar", status_code=status.HTTP_303_SEE_OTHER)
    senha_hash = obter_hash_senha(senha)
    usuario = Usuario(
        nome=nome,
        sobrenome=sobrenome,
        email=email,
        telefone=telefone,
        senha=senha_hash,
        perfil=perfil)
    usuario_id= (UsuarioRepo.inserir(usuario)).id
    print(usuario_id)
    endereco = Endereco(
        id_usuario=usuario_id,
        endereco_cep= cep,
        endereco_numero = numero,
        endereco_complemento=complemento,
        endereco_endereco=endereco,
        endereco_cidade = cidade,
        endereco_uf=uf  )

    UsuarioRepo.inserir_endereco(endereco)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/sair")
async def get_sair():
    response = RedirectResponse("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value="",
        max_age=1,
        httponly=True,
        samesite="lax")
    return response    

