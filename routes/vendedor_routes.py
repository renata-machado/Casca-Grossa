from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from models.estoque_model import Estoque
from models.produto_model import Produto
from repositories.categoria_repo import CategoriaRepo
from repositories.estoque_repo import EstoqueRepo
from repositories.produto_repo import ProdutoRepo
from util.auth import obter_usuario_logado

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/vendedor")
async def get_root(request: Request, usuario_logado=Depends(obter_usuario_logado)):
    produtos = EstoqueRepo.obter_por_produtor(usuario_logado.id) if usuario_logado else []
    return templates.TemplateResponse("pages/vendedor/index.html", {
        "request": request,
        "vendedor": usuario_logado,
        "produtos": produtos
    })


@router.get("/cadastrar_produto")
async def get_cadastrar_produto(request: Request):
    categorias = CategoriaRepo.listar()
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
    id_categoria: int = Form(...),
    usuario_logado=Depends(obter_usuario_logado)
):
    if not usuario_logado:
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

    produto = Produto(
        nome=nomeProduto,
        descricao=descricaoProduto,
        preco=precoProduto,
        quantidade=quantidadeProduto,
        id_categoria=id_categoria
    )

    # inserir produto e pegar o id gerado
    produto_criado = ProdutoRepo.inserir(produto)

    if produto_criado and produto_criado.id:
        estoque = Estoque(
            id_produto=produto_criado.id,
            id_produtor=usuario_logado.id,
            quantidade=quantidadeProduto
        )

        EstoqueRepo.inserir(estoque)

        return RedirectResponse(
            "/vendedor",
            status_code=status.HTTP_303_SEE_OTHER
        )

    return RedirectResponse(
        "/cadastrar_produto",
        status_code=status.HTTP_303_SEE_OTHER
    )
@router.post("/post_cadastrar_estoque")
async def post_cadastrar_estoque(
    id_produto: int = Form(...),
    quantidade: int = Form(...),
    usuario_logado=Depends(obter_usuario_logado)
):
    estoque = Estoque(
        id_produto=id_produto,
        id_produtor=usuario_logado.id,
        quantidade=quantidade
    )
    sucesso = EstoqueRepo.inserir(estoque)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Erro ao adicionar estoque.")
    return RedirectResponse("/vendedor", status_code=status.HTTP_303_SEE_OTHER)


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