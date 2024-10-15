from fastapi import APIRouter, Request, status
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/cliente")
async def get_root(request: Request):
    return templates.TemplateResponse("pages/cliente/index.html", {"request": request})

@router.get("/cliente/tela_compra")
async def get_root(request: Request):
    return templates.TemplateResponse("pages/cliente/tela_compra.html", {"request": request})

