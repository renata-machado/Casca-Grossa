from pathlib import Path
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from models.categoria_model import Categoria
from repositories.categoria_repo import CategoriaRepo
from repositories.estoque_repo import EstoqueRepo
from repositories.produto_repo import ProdutoRepo
from repositories.usuario_repo import UsuarioRepo
from routes.main_routes import router as main_router
from routes.cliente_routes import router as cliente_router
from routes.usuario_routes import router as usuario_router
from routes.vendedor_routes import router as vendedor_router
from util.auth import checar_autorizacao
from util.exceptions import tratar_excecoes

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# Criar todas as tabelas
UsuarioRepo.criar_tabela()
ProdutoRepo.criar_tabela()
CategoriaRepo.criar_tabela()
EstoqueRepo.criar_tabela()


# Inserir categorias padrão se banco estiver vazio
def criar_categorias_padrao():
    if not CategoriaRepo.listar():
        CategoriaRepo.inserir(Categoria(nome="Frutas", descricao="Frutas frescas"))
        CategoriaRepo.inserir(Categoria(nome="Verduras", descricao="Verduras frescas"))
        CategoriaRepo.inserir(Categoria(nome="Hortalicas", descricao="Hortalicas frescas"))


criar_categorias_padrao()

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
tratar_excecoes(app)


# Middleware para autorização
@app.middleware("http")
async def autorizacao_middleware(request: Request, call_next):
    await checar_autorizacao(request)
    response = await call_next(request)
    return response

# Middleware para autenticação
@app.middleware("http")
async def autenticacao_middleware(request: Request, call_next):
    from util.auth import checar_autenticacao

    await checar_autenticacao(request)
    response = await call_next(request)
    return response



app.include_router(main_router)
app.include_router(cliente_router)
app.include_router(usuario_router)
app.include_router(vendedor_router)