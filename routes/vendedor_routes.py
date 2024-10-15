from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from models.estoque_model import Estoque
from repositories.categoria_repo import CategoriaRepo
from repositories.estoque_repo import EstoqueRepo
from util.db import obter_conexao
from models.produto_model import Produto
from repositories.produto_repo import ProdutoRepo
from util.auth import obter_usuario_logado

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/vendedor")
async def get_root(request: Request, usuario_logado=Depends(obter_usuario_logado)):
    vendedor = usuario_logado
    return templates.TemplateResponse("pages/vendedor/index.html", {
        "request": request,
        "vendedor": vendedor
    })

@router.get("/cadastrar_produto")
async def cadastrar_produto(request: Request):
    db = obter_conexao()  # Conexão com o banco de dados
    categoria_repo = CategoriaRepo(db)  # Instância do repositório de categorias
    categorias = categoria_repo.listar()  # Listagem de categorias
    db.close()  # Fechar conexão com o banco

    return templates.TemplateResponse("pages/vendedor/cadastrar_produto.html", {
        "request": request,
        "categorias": categorias
    })

@router.post("/post_cadastrar_produto")
async def post_cadastrar_produto(
    request: Request,
    nomeProduto: str = Form(...),
    descricaoProduto: str = Form(...),
    precoProduto: float = Form(...),
    quantidadeProduto: int = Form(...),
    id_categoria: int = Form(...),  # Mudança para id_categoria
    id_produtor: int = Form(...)  # Adicione o id do produtor aqui
):
    try:
        # Crie uma instância do produto com os dados do formulário
        produto = Produto(
            nome=nomeProduto,
            descricao=descricaoProduto,
            preco=precoProduto,
            quantidade=quantidadeProduto,
            categoria=id_categoria  # Mudança para id_categoria
        )
        
        # Chame o método inserir para adicionar o produto ao banco de dados
        resultado_produto = ProdutoRepo.inserir(produto)

        if resultado_produto:
            # Crie uma instância de Estoque
            estoque = Estoque(
                id_produto=resultado_produto.id,
                id_produtor=id_produtor,
                quantidade=quantidadeProduto
            )
            # Insira o estoque
            EstoqueRepo.inserir(estoque)
            return RedirectResponse("/vendedor", status_code=status.HTTP_303_SEE_OTHER)
        
        return {"error": "Erro ao cadastrar o produto."}
    
    except Exception as e:
        return {"error": f"Erro ao cadastrar o produto: {str(e)}"}




@router.post("/post_cadastrar_estoque")
async def post_cadastrar_estoque(
    id_produto: int = Form(...),
    usuario_logado = Depends(obter_usuario_logado),  # Obtém o usuário autenticado
    quantidade: int = Form(...)
):
    id_produtor = usuario_logado.id  # Acesse o ID do usuário autenticado
    estoque = Estoque(id_produto=id_produto, id_produtor=id_produtor, quantidade=quantidade)

    # Insira o estoque no repositório (supondo que já tenha um método para isso)
    sucesso = EstoqueRepo.inserir(estoque)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Erro ao adicionar estoque.")
    
    return {"mensagem": "Estoque adicionado com sucesso."}

@router.get("/estoque/produtor/{id_produtor}")
async def obter_estoque_por_produtor(id_produtor: int):
    estoque = EstoqueRepo.obter_por_produtor(id_produtor)
    return {"estoque": estoque}

@router.put("/estoque/atualizar/{id}")
async def atualizar_estoque(id: int, quantidade: int):
    sucesso = EstoqueRepo.atualizar_quantidade(id, quantidade)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Erro ao atualizar estoque.")
    return {"mensagem": "Estoque atualizado com sucesso."}

@router.delete("/estoque/excluir/{id}")
async def excluir_estoque(id: int):
    sucesso = EstoqueRepo.excluir(id)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Erro ao excluir estoque.")
    return {"mensagem": "Estoque excluído com sucesso."}
