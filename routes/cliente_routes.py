from fastapi import APIRouter, Request, status
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/cliente")
async def get_root(request: Request):
    return templates.TemplateResponse("pages/cliente/index.html", {"request": request})

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
async def get_carrinho(request: Request):
    return templates.TemplateResponse("pages/cliente/compra.html", {"request": request})