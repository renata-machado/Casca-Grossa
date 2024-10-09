from typing import List, Optional
import sqlite3  # ou outro banco de dados que você está usando
from models.categoria_model import Categoria

class CategoriaRepo:
    def __init__(self, db_connection):
        self.connection = db_connection

    def inserir(self, categoria: Categoria) -> Optional[int]:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO categoria (nome, descricao) VALUES (?, ?)",
            (categoria.nome, categoria.descricao),
        )
        self.connection.commit()
        return cursor.lastrowid

    def listar(self) -> List[Categoria]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, nome, descricao FROM categoria")
        categoria = cursor.fetchall()
        return [Categoria(id=row[0], nome=row[1], descricao=row[2]) for row in categoria]

    def obter_por_id(self, id: int) -> Optional[Categoria]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, nome, descricao FROM categoria WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return Categoria(id=row[0], nome=row[1], descricao=row[2])
        return None

    def atualizar(self, categoria: Categoria) -> bool:
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE categoria SET nome = ?, descricao = ? WHERE id = ?",
            (categoria.nome, categoria.descricao, categoria.id),
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def excluir(self, id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM categoria WHERE id = ?", (id,))
        self.connection.commit()
        return cursor.rowcount > 0
