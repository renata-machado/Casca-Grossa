import sqlite3

# Instruções SQL para categoria
SQL_CRIAR_TABELA_CATEGORIA = """
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        descricao TEXT
    )
"""

SQL_INSERIR_CATEGORIA = """
    INSERT INTO categoria (nome, descricao)
    VALUES (?, ?)
"""

SQL_OBTER_CATEGORIA_POR_ID = """
    SELECT id, nome, descricao
    FROM categoria
    WHERE id=?
"""

SQL_ATUALIZAR_CATEGORIA = """
    UPDATE categoria
    SET nome=?, descricao=?
    WHERE id=?
"""

SQL_EXCLUIR_CATEGORIA = """
    DELETE FROM categoria
    WHERE id=?
"""