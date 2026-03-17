from typing import List, Optional
from models.categoria_model import Categoria
from util.db import obter_conexao


class CategoriaRepo:

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categoria (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE,
                    descricao TEXT
                )
            """)

    @classmethod
    def inserir(cls, categoria: Categoria) -> Optional[int]:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO categoria (nome, descricao) VALUES (?, ?)",
                (categoria.nome, categoria.descricao),
            )
            return cursor.lastrowid

    @classmethod
    def listar(cls) -> List[Categoria]:
        with obter_conexao() as db:
            cursor = db.cursor()
            rows = cursor.execute("SELECT id, nome, descricao FROM categoria").fetchall()
            return [Categoria(id=row[0], nome=row[1], descricao=row[2]) for row in rows]

    @classmethod
    def obter_por_id(cls, id: int) -> Optional[Categoria]:
        with obter_conexao() as db:
            cursor = db.cursor()
            row = cursor.execute(
                "SELECT id, nome, descricao FROM categoria WHERE id = ?", (id,)
            ).fetchone()
            if row:
                return Categoria(id=row[0], nome=row[1], descricao=row[2])
            return None

    @classmethod
    def atualizar(cls, categoria: Categoria) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                "UPDATE categoria SET nome = ?, descricao = ? WHERE id = ?",
                (categoria.nome, categoria.descricao, categoria.id),
            )
            return resultado.rowcount > 0

    @classmethod
    def excluir(cls, id: int) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute("DELETE FROM categoria WHERE id = ?", (id,))
            return resultado.rowcount > 0