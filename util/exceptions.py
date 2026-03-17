from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.mensagens import adicionar_mensagem_erro


templates = Jinja2Templates(directory="templates")


def tratar_excecoes(app: FastAPI):

    @app.exception_handler(status.HTTP_401_UNAUTHORIZED)
    async def unauthorized_exception_handler(request, exc):
        response = RedirectResponse("/entrar", status_code=status.HTTP_302_FOUND)
        adicionar_mensagem_erro(
            response,
            f"Você precisa estar autenticado para acessar {request.url.path}.",
        )
        return response

    @app.exception_handler(status.HTTP_403_FORBIDDEN)
    async def forbidden_exception_handler(request, exc):
        usuario = request.state.usuario if hasattr(request.state, "usuario") else None
        response = RedirectResponse("/entrar", status_code=status.HTTP_302_FOUND)
        nome = usuario.nome if usuario else "desconhecido"
        adicionar_mensagem_erro(
            response,
            f"Você está logado como {nome} e seu perfil não tem permissão para acessar {request.url.path}.",
        )
        return response

    @app.exception_handler(404)
    async def not_found_exception_handler(request, exc):
        return templates.TemplateResponse(
            "pages/404.html", {"request": request}, status_code=404
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        dados = {
            "request": request,
            "detail": f"Erro na requisição HTTP:<br>{type(exc).__name__}: {exc}",
            "status_code": exc.status_code
        }
        return templates.TemplateResponse("pages/erro.html", dados)

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        dados = {
            "request": request,
            "detail": f"Erro interno do servidor.<br>{type(exc).__name__}: {exc}",
            "status_code": 500
        }
        return templates.TemplateResponse("pages/erro.html", dados)