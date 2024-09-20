from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates =Jinja2Templates(directory="templates")

@router.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse("pages/tela_inicial.html", {"request":request})

@router.get("/cadastro")
async def get_cadastro(request: Request):
    return templates.TemplateResponse("pages/Cadastro.html", {"request":request})

@router.get("/entre")
async def get_entre(request: Request):
    return templates.TemplateResponse("pages/Entre.html", {"request":request})

@router.get("/telaCompra")
async def get_telaCompra(request: Request):
    return templates.TemplateResponse("pages/tela_compra.html", {"request":request})