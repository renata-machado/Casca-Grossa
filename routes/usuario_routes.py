from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from models.endereco_model import Endereco
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import conferir_senha, obter_hash_senha
from util.cookies import excluir_cookie_auth

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/usuario/sobre")
async def get_sobre(request: Request):
    return templates.TemplateResponse("pages/usuario/sobre.html", {"request": request})


@router.get("/usuario/dados")
async def get_dados(request: Request):
    return templates.TemplateResponse("pages/usuario/tela_dados.html", {"request": request})


@router.post("/usuario/post_dados")
async def post_dados(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...)):
    id_usuario = request.state.usuario.id
    usuario = Usuario(
        id=id_usuario,
        nome=nome,
        email=email,
        telefone=telefone)
    UsuarioRepo.atualizar_dados(usuario)
    return RedirectResponse(url="/perfil", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/usuario/endereco")
async def get_endereco(request: Request):
    return templates.TemplateResponse("pages/usuario/endereco.html", {"request": request})


@router.post("/usuario/post_endereco")
async def post_endereco(
    request: Request,
    cep: str = Form(...),
    numero: str = Form(...),
    complemento: str = Form(""),
    logradouro: str = Form(...),
    cidade: str = Form(...),
    uf: str = Form(...)):
    id_usuario = request.state.usuario.id
    endereco = Endereco(
        id_usuario=id_usuario,
        endereco_cep=cep,
        endereco_numero=numero,
        endereco_complemento=complemento,
        endereco_endereco=logradouro,
        endereco_cidade=cidade,
        endereco_uf=uf)
    UsuarioRepo.atualizar_endereco(endereco)
    return RedirectResponse(url="/perfil", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/usuario/senha")
async def get_senha(request: Request):
    return templates.TemplateResponse("pages/usuario/senha.html", {"request": request})


@router.post("/usuario/post_senha")
async def post_senha(
    request: Request,
    senha_atual: str = Form(...),
    nova_senha: str = Form(...),
    conf_nova_senha: str = Form(...)):
    id_usuario = request.state.usuario.id
    usuario = UsuarioRepo.obter_por_id(id_usuario)

    if nova_senha != conf_nova_senha:
        return RedirectResponse(url="/usuario/senha", status_code=status.HTTP_303_SEE_OTHER)

    if not conferir_senha(senha_atual, usuario.senha):
        return RedirectResponse(url="/usuario/senha", status_code=status.HTTP_303_SEE_OTHER)

    nova_senha_hash = obter_hash_senha(nova_senha)
    UsuarioRepo.atualizar_senha(id_usuario, nova_senha_hash)
    return RedirectResponse(url="/perfil", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/sair")
async def get_sair():
    response = RedirectResponse(url="/entrar", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    return excluir_cookie_auth(response)


@router.get("/perfil")
async def get_perfil(request: Request):
    return templates.TemplateResponse("pages/usuario/tela_dados.html", {"request": request})


@router.get("/politicaPrivacidade")
async def get_politicaPrivacidade(request: Request):
    return templates.TemplateResponse("pages/usuario/politica_privacidade.html", {"request": request})