from datetime import date
from typing import Optional
from models.endereco_model import Endereco
from models.usuario_model import Usuario
from sql.usuario_sql import *
from util.auth import conferir_senha
from util.db import obter_conexao


class UsuarioRepo:
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def obter_por_id(cls, id: int) -> Optional[Usuario]:
        with obter_conexao() as db:
            cursor = db.cursor()
            dados = cursor.execute(
                SQL_OBTER_POR_ID, (id,)).fetchone()
            if dados:
                return Usuario(*dados)
            return None

    @classmethod
    def inserir(cls, usuario: Usuario) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(SQL_INSERIR_USUARIO,
                (usuario.nome, 
                 usuario.sobrenome,
                 usuario.email, 
                 usuario.telefone,
                 usuario.senha, 
                 usuario.perfil 
                 ))
            if cursor.rowcount > 0:
                    usuario.id = cursor.lastrowid
                    return usuario
           
    
    @classmethod
    def inserir_endereco(cls, endereco: Endereco) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(SQL_INSERIR_ENDERECO,
                (endereco.id_usuario,
                 endereco.endereco_cep,
                 endereco.endereco_numero,
                 endereco.endereco_complemento,
                 endereco.endereco_endereco,
                 endereco.endereco_cidade,
                 endereco.endereco_uf
                 
                 ))
            return resultado.rowcount > 0
    
    
    @classmethod
    def atualizar_endereco(cls, usuario: Usuario) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(SQL_ATUALIZAR_ENDERECO,
                (usuario.endereco_cep,
                usuario.endereco_numero,
                usuario.endereco_complemento,
                usuario.endereco_endereco,
                usuario.endereco_cidade,
                usuario.endereco_uf,
                usuario.id))
            return resultado.rowcount > 0
        
    @classmethod
    def atualizar_dados(cls, usuario: Usuario) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_ATUALIZAR_DADOS, (
                    usuario.nome, 
                    usuario.email, 
                    usuario.telefone, 
                    usuario.id))
            return resultado.rowcount > 0
    
    @classmethod
    def atualizar_senha(cls, id: int, senha: str) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_ATUALIZAR_SENHA, (senha, id))
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
    def excluir_usuario(cls, id: int) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_EXCLUIR_USUARIO, (id,))
            return resultado.rowcount > 0    