from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi import Form
from models.categoria_model import Categoria
from repositories.categoria_repo import CategoriaRepo
from util.db import *

router = APIRouter()

@router.post("/categoria/")
async def criar_categoria(
    nome: str = Form(...),
    descricao: str = Form(...)
):
    db = obter_conexao()  # Obtenha a conexão do banco de dados
    categoria = Categoria(nome=nome, descricao=descricao)
    categoria_id = CategoriaRepo.inserir(categoria)
    return RedirectResponse("/", status_code=303)
