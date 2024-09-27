SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        perfil INT NOT NULL      
        )
"""

SQL_CRIAR_TABELA_ENDERECO = """
    CREATE TABLE IF NOT EXISTS endereco (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTERGER, 
    endereco_cep TEXT NULL,
    endereco_logradouro TEXT NULL,
    endereco_numero TEXT NULL,
    endereco_complemento TEXT NULL,
    endereco_bairro TEXT NULL,
    endereco_cidade TEXT NULL,
    endereco_uf TEXT NULL),
    CONSTRAINT fk_id_usuario_endereco FOREIGN KEY (id_usuario) REFERENCES usuario (id)
"""



SQL_INSERIR_USUARIO = """
    INSERT INTO usuario(id, nome, email, senha, perfil)
    VALUES (?, ?, ?)
"""


SQL_INSERIR_ENDERECO = """
    INSERT INTO usuario 
    (id_usuario, endereco_cep, endereco_logradouro, endereco_numero, endereco_complemento, endereco_bairro, endereco_cidade, endereco_uf)
    VALUES (?, ?, ?, ?, ?,?, ?)
    WHERE id=?
"""


SQL_CHECAR_CREDENCIAIS = """
    SELECT nome, email, perfil, senha
    FROM usuario
    WHERE email = ?
"""

SQL_ATUALIZAR_DADOS = """
    UPDATE usuario
    SET nome = ?, email = ?, telefone = ?
    WHERE email = ?
"""


SQL_ATUALIZAR_ENDERECO = """
    UPDATE usuario SET
    SET endereco_cep=? 
    endereco_logradouro=?
    endereco_numero=? 
    endereco_complemento=? 
    endereco_bairro=? 
    endereco_cidade=? 
    endereco_uf=?
    WHERE id = ?
"""

SQL_ATUALIZAR_SENHA = """
    UPDATE usuario
    SET senha = ?
    WHERE email = ?
"""

SQL_ATUALIZAR_TEMA = """
    UPDATE usuario
    SET tema = ?
    WHERE email = ?
"""

SQL_EXCLUIR_USUARIO = """
    DELETE FROM usuario
    WHERE email = ?
"""