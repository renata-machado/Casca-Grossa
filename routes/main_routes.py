from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from util.templates import obter_jinja_templates

router = APIRouter()
templates = obter_jinja_templates("templates/main")


@router.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/inicio.html", {"request": request})

@router.get("/confEmail", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/confEmail.html", {"request": request})

@router.get("/faq", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/faq.html", {"request": request})

@router.get("/senha", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/senha.html", {"request": request})