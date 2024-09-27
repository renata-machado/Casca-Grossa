from datetime import date
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import conferir_senha


router = APIRouter(prefix="/usuario")

templates = Jinja2Templates(directory="templates")

@router.get("/sobre")
async def get_sobre(request: Request):    
    return templates.TemplateResponse("pages/usuario/sobre.html", {"request": request})

@router.get("/tema")
async def get_tema(request: Request):
    temas = ["default", "cerulean", "cosmo", "cyborg", "darkly", "flatly", "journal", "litera", "lumen", "lux", "materia", "minty", "morph", "pulse", "quartz", "sandstone", "simplex", "sketchy", "slate", "solar", "spacelab", "superhero", "united", "vapor", "yeti", "zephyr"]
    return templates.TemplateResponse("pages/usuario/tema.html", {"request": request, "temas": temas})

@router.post("/post_tema")
async def post_tema(tema: str = Form(...)):
    response = RedirectResponse("/usuario/tema", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="tema",
        value=tema,
        max_age=3600*24*365*10,
        httponly=True,
        samesite="lax"
    )
    return response

@router.get("/dados")
async def get_dados(request: Request):    
    return templates.TemplateResponse("pages/usuario/dados.html", {"request": request})

@router.post("/post_dados")
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
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/endereco")
async def get_endereco(request: Request):    
    return templates.TemplateResponse("pages/usuario/endereco.html", {"request": request})

@router.post("/post_endereco")
async def post_dados(
    request: Request, 
    cep: str = Form(...),
    numero: str = Form(...),
    complemento: str = Form(),
    endereco: str = Form(...),
    cidade: str = Form(...),
    uf: str = Form(...)):
    id_usuario = request.state.usuario.id
    usuario = Usuario(
        id=id_usuario,
        cep=cep,
        numero=numero,
        complemento=complemento,
        endereco=endereco,
        cidade=cidade,
        uf=uf)
    UsuarioRepo.atualizar_endereco(usuario)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/senha")
async def get_dados(request: Request):    
    return templates.TemplateResponse("pages/usuario/senha.html", {"request": request})

@router.post("/post_senha")
async def post_senha(
    request: Request, 
    senha_atual: str = Form(...),    
    nova_senha: str = Form(...),
    conf_nova_senha: str = Form(...)):
    id_usuario = request.state.usuario.id
    usuario = UsuarioRepo.obter_por_id(id_usuario)    
    if nova_senha == conf_nova_senha and conferir_senha(senha_atual, usuario.senha):
        UsuarioRepo.atualizar_senha(id_usuario, nova_senha)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)