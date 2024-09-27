import sqlite3
from typing import Optional
from models.usuario_model import Usuario
from models.endereco_model import Endereco
from sql.usuario_sql import *
from util.auth import conferir_senha
from util.db import obter_conexao

class UsuarioRepo:
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, usuario: Usuario) -> Optional[Usuario]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR_USUARIO,
                    (
                        usuario.id,
                        usuario.nome,
                        usuario.sobrenome,
                        usuario.senha,
                        usuario.perfil,
                    ),
                )
                if cursor.rowcount > 0:
                    return usuario
        except sqlite3.Error as ex:
            print(ex)
            return None
    @classmethod
    def inserir_endereco(cls, endereco: Endereco) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(SQL_INSERIR_ENDERECO,
                (endereco.endereco_cep,
                 endereco.endereco_logradouro,
                 endereco.endereco_numero,
                 endereco.endereco_complemento,
                 endereco.endereco_bairro,
                 endereco.endereco_cidade,
                 endereco.endereco_uf,
                 endereco.id_usuario
                ))
            return resultado.rowcount > 0
        
    @classmethod
    def atualizar_dados(cls, nome: str, email: str, telefone: str) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_ATUALIZAR_DADOS, (nome, email, telefone, email))
            return resultado.rowcount > 0
    
    @classmethod
    def atualizar_senha(cls, email: str, senha: str) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_ATUALIZAR_SENHA, (senha, email))
            return resultado.rowcount > 0
    
    @classmethod
    def atualizar_tema(cls, email: str, tema: str) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_ATUALIZAR_TEMA, (tema, email))
            return resultado.rowcount > 0
      
    @classmethod
    def checar_credenciais(cls, email: str, senha: str) -> Optional[tuple]:
        with obter_conexao() as db:
            cursor = db.cursor()
            dados = cursor.execute(
                SQL_CHECAR_CREDENCIAIS, (email,)).fetchone()
            if dados:
                if conferir_senha(senha, dados[3]):
                    return (dados[0], dados[1], dados[2])
            return None
    
    @classmethod
    def excluir_usuario(cls, email: str) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_EXCLUIR_USUARIO, (email,))
            return resultado.rowcount > 0    