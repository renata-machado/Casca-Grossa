# from fastapi import Depends, FastAPI
# from fastapi.staticfiles import StaticFiles
# import uvicorn
# from repositories.usuario_repo import UsuarioRepo
# from routes import main_routes
# from util.auth import checar_permissao, middleware_autenticacao
# from util.exceptions import configurar_excecoes

# UsuarioRepo.criar_tabela()
# app = FastAPI(dependencies=[Depends(checar_permissao)])
# app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
# app.middleware(middleware_type="http")(middleware_autenticacao)
# configurar_excecoes(app)
# app.include_router(main_routes.router)

# if __name__ == "__main__":
#     uvicorn.run(app="main:app", port=8000, reload=True)

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from repositories.usuario_repo import UsuarioRepo
from routes.main_routes import router as main_router
from routes.cliente_routes import router as cliente_router
from routes.usuario_routes import router as usuario_router
from routes.vendedor_routes import router as vendedor_router
from sql.estoque_sql import SQL_CRIAR_TABELA_ESTOQUE
from sql.usuario_sql import *
from sql.produto_sql import *
from sql.categoria_sql import *

import sqlite3

from util.auth import checar_autenticacao, checar_autorizacao
from util.exceptions import tratar_excecoes

load_dotenv()
UsuarioRepo.criar_tabela()
app = FastAPI(dependencies=[Depends(checar_autorizacao)])
app.mount("/static", StaticFiles(directory="static"), name="static")
app.middleware("http")(checar_autenticacao)
tratar_excecoes(app)

app.include_router(main_router)
app.include_router(cliente_router)
app.include_router(usuario_router)
app.include_router(vendedor_router)







# def criar_categoria_padrao(db: sqlite3.Connection):
#     cursor = db.cursor()
#     categoria_padrao = [
#         ("Frutas", "Frutas"),
#         ("Verduras", "Verduras"),
#         ("Hortalicas", "Hortalicas")
#     ]
    
#     for nome, descricao in categoria_padrao:
#         cursor.execute(
#             "INSERT INTO categoria (nome, descricao) VALUES (?, ?)",
#             (nome, descricao)
#         )
    
#     db.commit()



# conn = sqlite3.connect('dados.db')
# cursor = conn.cursor()
# # Criar a tabela
# cursor.execute(SQL_CRIAR_TABELA)
# cursor.execute(SQL_CRIAR_TABELA_ENDERECO)
# cursor.execute(SQL_CRIAR_TABELA_PRODUTO)
# cursor.execute(SQL_CRIAR_TABELA_CATEGORIA)
# cursor.execute(SQL_CRIAR_TABELA_ESTOQUE)
# criar_categoria_padrao(conn)
# conn.close()