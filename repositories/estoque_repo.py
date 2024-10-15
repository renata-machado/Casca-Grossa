from models.estoque_model import Estoque
from sql.estoque_sql import *
from util.db import obter_conexao


   


class EstoqueRepo:
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_CRIAR_TABELA_ESTOQUE)

    @classmethod
    def inserir(cls, estoque: Estoque) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(SQL_INSERIR_ESTOQUE, (estoque.id_produto, estoque.id_produtor, estoque.quantidade))
            return resultado.rowcount > 0

    @classmethod
    def obter_por_produtor(cls, id_produtor: int):
        with obter_conexao() as db:
            cursor = db.cursor()
            return cursor.execute(
                "SELECT * FROM estoque WHERE id_produtor = ?", (id_produtor,)
            ).fetchall()

    @classmethod
    def atualizar_quantidade(cls, id: int, quantidade: int) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                "UPDATE estoque SET quantidade = ? WHERE id = ?", (quantidade, id)
            )
            return resultado.rowcount > 0

    @classmethod
    def excluir(cls, id: int) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                "DELETE FROM estoque WHERE id = ?", (id,)
            )
            return resultado.rowcount > 0
