from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from util.mensagens import adicionar_mensagem_erro


templates = Jinja2Templates(directory="templates")


def tratar_excecoes(app: FastAPI):

    @app.exception_handler(401)
    async def unauthorized_exception_handler(request, exc):
        return_url = f"?return_url={request.url.path}"
        response = RedirectResponse(f"/{return_url}")
        adicionar_mensagem_erro(
            response,
            f"Você precisa estar autenticado para acessar a página do endereço {request.url.path}.",
        )
        return response

    @app.exception_handler(403)
    async def forbidden_exception_handler(request, exc):
        usuarioAutenticadoDto = request.state.usuario
        return_url = f"?return_url={request.url.path}"
        response = RedirectResponse(f"/post_entrar{return_url}")
        adicionar_mensagem_erro(
            response,
            f"Você está logado como {usuarioAutenticadoDto.nome} e seu perfil de usuário não tem permissão para acessar a página do endereço {request.url.path}. Entre com as credenciais de um perfil compatível.",
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
        return templates.TemplateResponse(
            "pages/erro.html", dados)

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        dados = {
            "request": request,
            "detail": f"Erro interno do servidor.<br>{type(exc).__name__}: {exc}",
            "status_code": 500
        }
        return templates.TemplateResponse("pages/erro.html", dados)

# import logging
# from fastapi import FastAPI, HTTPException, Request, status
# from fastapi.responses import RedirectResponse
# from util.cookies import adicionar_mensagem_erro
# from util.templates import obter_jinja_templates

# templates = obter_jinja_templates("templates/public")
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# def configurar_excecoes(app: FastAPI):

#     @app.exception_handler(401)
#     async def unauthorized_exception_handler(request: Request, _):
#         return_url = f"?return_url={request.url.path}"
#         response = RedirectResponse(
#             f"/entrar{return_url}", status_code=status.HTTP_302_FOUND
#         )
#         adicionar_mensagem_erro(
#             response,
#             f"A página <b>{request.url.path}</b> é restrita a usuários logados. Identifique-se para poder prosseguir.",
#         )
#         return response

#     @app.exception_handler(403)
#     async def forbidden_exception_handler(request: Request, _):
#         return_url = f"?return_url={request.url.path}"
#         usuario = request.state.usuario if hasattr(request.state, "usuario") else None

#         if usuario:
#             match usuario.perfil:
#                 case 1:
#                     return_url = "/usuario"
#                 case 2:
#                     return_url = "/admin"
#             response = RedirectResponse(return_url, status_code=status.HTTP_302_FOUND)
#             adicionar_mensagem_erro(
#                 response,
#                 f"Você está logado como <b>{usuario.nome}</b> e seu perfil de usuário não tem autorização de acesso à página <b>{request.url.path}</b>. Saia de seu usuário e entre com um usuário do perfil adequado para poder acessar a página em questão.",
#             )
#             return response
#         else:
#             response = RedirectResponse(
#                 f"/entrar{return_url}", status_code=status.HTTP_302_FOUND
#             )
#             adicionar_mensagem_erro(
#                 response,
#                 f"Somente usuários autenticados possuem acesso à página <b>{request.url.path}</b>. Entre com um usuário do perfil adequado para poder acessar a página em questão.",
#             )
#             return response

#     @app.exception_handler(404)
#     async def page_not_found_exception_handler(request: Request, _):
#         usuario = request.state.usuario if hasattr(request.state, "usuario") else None
#         return templates.TemplateResponse(
#             "pages/404.html",
#             {
#                 "request": request,
#                 "usuario": usuario,
#             },
#         )

#     @app.exception_handler(HTTPException)
#     async def http_exception_handler(request: Request, ex: HTTPException):
#         logger.error("Ocorreu uma exceção não tratada: %s", ex)
#         usuario = request.state.usuario if hasattr(request.state, "usuario") else None
#         view_model = {
#             "request": request,
#             "usuario": usuario,
#             "detail": "Erro na requisição HTTP.",
#         }
#         return templates.TemplateResponse(
#             "pages/error.html",
#             view_model,
#             status_code=ex.status_code,
#         )

#     @app.exception_handler(Exception)
#     async def general_exception_handler(request: Request, ex: Exception):
#         logger.error("Ocorreu uma exceção não tratada: %s", ex)
#         usuario = request.state.usuario if hasattr(request.state, "usuario") else None
#         view_model = {
#             "request": request,
#             "usuario": usuario,
#             "detail": "Erro interno do servidor.",
#         }
#         return templates.TemplateResponse(
#             "pages/error.html",
#             view_model,
#             status_code=500,
#         )
