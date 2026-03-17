import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Request, status
from dtos.usuario_autenticado import UsuarioAutenticado

NOME_COOKIE_AUTH = "token"
JWT_SECRET = os.getenv("JWT_SECRET", "mysecret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
TOKEN_EXPIRATION_HOURS = int(os.getenv("TOKEN_EXPIRATION_HOURS", "24"))

ROTAS_PUBLICAS = ["/", "/entrar", "/cadastrar", "/post_entrar", "/post_cadastrar",
                  "/sobreNos", "/ajuda", "/static"]


async def obter_usuario_logado(request: Request) -> UsuarioAutenticado | None:
    try:
        token = request.cookies.get(NOME_COOKIE_AUTH)

        if not token or token.strip() == "":
            return None

        dados = validar_token(token)

        if dados.get("mensagem"):
            return None

        usuario = UsuarioAutenticado(
        id=dados.get("id"),
        nome=dados.get("nome"),
        email=dados.get("email"),
        perfil=dados.get("perfil"),
        telefone=dados.get("telefone")
    )

        return usuario

    except (KeyError, ValueError, TypeError):
        return None

async def checar_autenticacao(request: Request):
    usuario = await obter_usuario_logado(request)
    request.state.usuario = usuario
 


async def checar_autorizacao(request: Request):
    usuario = request.state.usuario if hasattr(request.state, "usuario") else None

    for rota in ROTAS_PUBLICAS:
        if request.url.path.startswith(rota):
            return

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    area_do_usuario = request.url.path.startswith("/usuario")
    area_do_vendedor = request.url.path.startswith("/vendedor")
    area_do_cliente = request.url.path.startswith("/cliente")

    if area_do_usuario and not usuario.perfil:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if area_do_vendedor and usuario.perfil != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if area_do_cliente and usuario.perfil != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def obter_hash_senha(senha: str) -> str:
    try:
        hashed = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
        return hashed.decode()
    except ValueError:
        return ""


def conferir_senha(senha: str, hash_senha: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode(), hash_senha.encode())
    except ValueError:
        return False


def criar_token(id: int, nome: str, email: str, perfil: int, telefone: str) -> str:
    expiracao = datetime.now() + timedelta(hours=TOKEN_EXPIRATION_HOURS)

    payload = {
        "id": id,
        "nome": nome,
        "email": email,
        "perfil": perfil,
        "telefone": telefone,
        "exp": expiracao
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def validar_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"nome": None, "email": None, "perfil": 0, "telefone": None, "mensagem": "Token expirado"}
    except jwt.InvalidTokenError:
        return {"nome": None, "email": None, "perfil": 0, "telefone": None, "mensagem": "Token inválido"}
    except Exception:
        return {"nome": None, "email": None, "perfil": 0, "telefone": None, "mensagem": "Token inválido"}


def criar_cookie_auth(response, token):
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value=token,
        max_age=TOKEN_EXPIRATION_HOURS * 3600,
        httponly=True,
        samesite="lax",
        secure=os.getenv("ENVIRONMENT") == "production"
    )
    return response

