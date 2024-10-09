from typing import Optional
from models.produto_model import Produto  # Certifique-se de que o modelo Produto está definido corretamente
from sql.produto_sql import *
from util.db import obter_conexao


class ProdutoRepo:
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_CRIAR_TABELA_PRODUTO)

    @classmethod
    def inserir(cls, produto: Produto) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(SQL_INSERIR_PRODUTO,
                (produto.nome,
                 produto.descricao,
                 produto.preco,
                 produto.quantidade,
                 produto.categoria                 ))
            if cursor.rowcount > 0:
                produto.id = cursor.lastrowid
                return True
            return False

    @classmethod
    def obter_por_id(cls, id: int) -> Optional[Produto]:
        with obter_conexao() as db:
            cursor = db.cursor()
            dados = cursor.execute(SQL_OBTER_PRODUTO_POR_ID, (id,)).fetchone()
            if dados:
                return Produto(*dados)
            return None

    @classmethod
    def atualizar(cls, produto: Produto) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(SQL_ATUALIZAR_PRODUTO,
                (produto.nome,
                 produto.descricao,
                 produto.preco,
                 produto.quantidade,
                 produto.categoria,
                 produto.id))
            return resultado.rowcount > 0

    @classmethod
    def excluir(cls, id: int) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(SQL_EXCLUIR_PRODUTO, (id,))
            return resultado.rowcount > 0
