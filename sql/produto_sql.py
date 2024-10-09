import sqlite3

# Instruções SQL
SQL_CRIAR_TABELA_PRODUTO = """
CREATE TABLE IF NOT EXISTS produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    preco REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    id_categoria INTEGER,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id)  -- Adicionando a chave estrangeira
)
"""

SQL_INSERIR_PRODUTO = """
INSERT INTO produto (nome, descricao, preco, quantidade, id_categoria)
VALUES (?, ?, ?, ?, ?)
"""

SQL_OBTER_PRODUTO_POR_ID = """
SELECT id, nome, descricao, preco, quantidade, id_categoria
FROM produto
WHERE id=?
"""

SQL_ATUALIZAR_PRODUTO = """
UPDATE produto
SET nome=?, descricao=?, preco=?, quantidade=?, id_categoria=?
WHERE id=?
"""

SQL_EXCLUIR_PRODUTO = """
DELETE FROM produto
WHERE id=?
"""
