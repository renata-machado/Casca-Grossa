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

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.main_routes import router as main_router
from sql.usuario_sql import *
import sqlite3

app = FastAPI()

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

app.include_router(main_router)








# conn = sqlite3.connect('dados.db')
# cursor = conn.cursor()

# # Criar a tabela
# cursor.execute(SQL_CRIAR_TABELA)

# conn.close()