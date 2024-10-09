import sqlite3


SQL_CRIAR_TABELA_ESTOQUE = """
CREATE TABLE IF NOT EXISTS estoque (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_produto INTEGER NOT NULL,
    id_produtor INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY (id_produto) REFERENCES produto(id),
    FOREIGN KEY (id_produtor) REFERENCES usuario(id)
)
"""


SQL_INSERIR_ESTOQUE = """
INSERT INTO estoque (id_produto, id_produtor, quantidade)
VALUES (?, ?, ?)
"""
