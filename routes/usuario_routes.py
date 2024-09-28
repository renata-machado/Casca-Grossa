from datetime import date
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import conferir_senha


router = APIRouter(prefix="")

templates = Jinja2Templates(directory="templates")

@router.get("/usuario/sobre")
async def get_sobre(request: Request):    
    return templates.TemplateResponse("pages/usuario/sobre.html", {"request": request})


@router.get("/usuario/dados")
async def get_dados(request: Request):    
    return templates.TemplateResponse("pages/usuario/dados.html", {"request": request})

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
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/usuario/endereco")
async def get_endereco(request: Request):    
    return templates.TemplateResponse("pages/usuario/endereco.html", {"request": request})

@router.post("/usuario/post_endereco")
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

@router.get("/usuario/senha")
async def get_dados(request: Request):    
    return templates.TemplateResponse("pages/usuario/senha.html", {"request": request})

@router.post("/usuario/post_senha")
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