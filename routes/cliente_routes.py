from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from repositories.produto_repo import ProdutoRepo
from repositories.estoque_repo import EstoqueRepo
from repositories.usuario_repo import UsuarioRepo
from models.usuario_model import Usuario
from models.endereco_model import Endereco
from util.auth import obter_usuario_logado


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/cliente")
async def get_root(request: Request):
    produtos = ProdutoRepo.obter_todos()
    return templates.TemplateResponse("pages/cliente/index.html", {"request": request, "produtos": produtos})

@router.get("/tela_compra")
async def get_tela_compra(request: Request):
    return templates.TemplateResponse("pages/cliente/tela_compra.html", {"request": request})

@router.get("/pedidos")
async def get_pedidos(request: Request):
    return templates.TemplateResponse("pages/cliente/pedidos.html", {"request": request})

@router.get("/favoritos")
async def get_favoritos(request: Request):
    return templates.TemplateResponse("pages/cliente/favoritos.html", {"request": request})

@router.get("/carrinho")
async def get_carrinho(request: Request):
    return templates.TemplateResponse("pages/cliente/carrinho.html", {"request": request})

@router.get("/compra")
async def get_compra(request: Request, usuario_logado=Depends(obter_usuario_logado)):
    return templates.TemplateResponse("pages/cliente/compra.html", {"request": request, "usuario": usuario_logado})

@router.post("/post_compra")
async def post_compra(
    request: Request,
    usuario_logado=Depends(obter_usuario_logado)
):
    # Aqui seria a lógica para processar a compra
    # Atualmente apenas redireciona para pedidos
    return RedirectResponse("/pedidos", status_code=status.HTTP_303_SEE_OTHER)