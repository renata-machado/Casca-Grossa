SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT NOT NULL,
    sobrenome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    telefone TEXT NOT NULL UNIQUE, 
    senha TEXT NOT NULL,
    perfil INTEGER NOT NULL)
"""

SQL_CRIAR_TABELA_ENDERECO = """
    CREATE TABLE IF NOT EXISTS endereco (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    id_usuario INTEGER ,
    endereco_cep TEXT,
    endereco_numero TEXT,
    endereco_complemento TEXT,
    endereco_endereco TEXT,
    endereco_cidade TEXT,
    endereco_uf TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
    )
    
"""

SQL_OBTER_POR_ID = """
    SELECT id, nome, email, telefone, senha, perfil, endereco_cep, endereco_numero, endereco_complemento, endereco_endereco, endereco_cidade, endereco_uf
    FROM usuario
    WHERE id=?
"""

SQL_INSERIR_USUARIO = """
    INSERT INTO usuario (nome, sobrenome,email, telefone,senha, perfil )
VALUES (?, ?, ?, ?, ?, ? )

"""


SQL_INSERIR_ENDERECO = """
    INSERT INTO endereco (id_usuario,endereco_cep, endereco_numero, endereco_complemento, endereco_endereco, endereco_cidade, endereco_uf )
VALUES (?, ?, ?, ?, ?, ?, ?)

"""

SQL_CHECAR_CREDENCIAIS = """
SELECT nome, email, perfil, telefone,senha
FROM usuario
WHERE email = ?
"""

SQL_ATUALIZAR_DADOS = """
    UPDATE usuario
    SET nome=?, email=?, telefone=?
    WHERE id=?
"""
SQL_ATUALIZAR_ENDERECO = """
    UPDATE endereco
    SET endereco_cep=?,
        endereco_numero=?,
        endereco_complemento=?,
        endereco_endereco=?,
        endereco_cidade=?,
        endereco_uf=?
    WHERE id_usuario=?  -- Ou WHERE id=? se você estiver usando o ID do endereço
"""


SQL_ATUALIZAR_SENHA = """
    UPDATE usuario
    SET senha=?
    WHERE id=?
"""


SQL_EXCLUIR_USUARIO = """
    DELETE FROM usuario
    WHERE id=?
"""