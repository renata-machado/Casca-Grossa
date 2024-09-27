from fastapi import APIRouter, Request, status
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/vendedor")

templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse("pages/vendedor/index.html", {"request": request})