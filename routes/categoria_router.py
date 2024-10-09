from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi import Form
from typing import List
from models.categoria_model import Categoria
from repositories.categoria_repo import CategoriaRepo
from util.db import *  # Assumindo que você tenha uma função para obter a conexão do banco de dados

router = APIRouter()

@router.post("/categoria/")
async def criar_categoria(
    nome: str = Form(...),
    descricao: str = Form(...)
):
    db = obter_conexao()  # Obtenha a conexão do banco de dados
    categoria = Categoria(nome=nome, descricao=descricao)
    categoria_id = CategoriaRepo(db).inserir(categoria)
    return RedirectResponse("/categoria", status_code=303)
