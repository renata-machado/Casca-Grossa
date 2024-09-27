from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates =Jinja2Templates(directory="templates")

@router.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse("pages/Entre.html", {"request":request})

@router.get("/cadastro")
async def get_cadastro(request: Request):
    return templates.TemplateResponse("pages/Cadastro.html", {"request":request})

@router.get("/PaginaPrincipal")
async def get_PPRINCIPAL(request: Request):
    return templates.TemplateResponse("pages/tela_inicial.html", {"request":request})

@router.get("/compra")
async def get_telaCompra(request: Request):
    return templates.TemplateResponse("pages/tela_compra.html", {"request":request})

@router.get("/form_cadastro")
async def get_Formcadastro(request: Request):
    return templates.TemplateResponse("pages/form_cadastro.html", {"request":request})

@router.get("/carrinho")
async def get_carrinho(request: Request):
    return templates.TemplateResponse("pages/carrinho.html", {"request":request})