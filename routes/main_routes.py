from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates =Jinja2Templates(directory="templates")

@router.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse("pages/tela_inicial.html", {"request":request})
@router.get("/entrar")
async def get_root(request: Request):
    return templates.TemplateResponse("pages/Entre.html", {"request":request})
@router.get("/cadastrar")
async def get_root(request: Request):
    return templates.TemplateResponse("pages/Cadastro.html", {"request":request})
@router.get("/form_cadastro")
async def get_root(request: Request):
    return templates.TemplateResponse("pages/form_cadastro.html", {"request":request})