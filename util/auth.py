import os
from typing import Optional
import bcrypt
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Header, Request, status
from dtos.usuario_autenticado import UsuarioAutenticado

# Definir variáveis diretamente no código
JWT_SECRET = "mysecret"  # Substitua "mysecret" pelo seu segredo
JWT_ALGORITHM = "HS256"   # Algoritmo utilizado

NOME_COOKIE_AUTH = "jwt-token"

async def obter_usuario_logado(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Token não fornecido.")

    token = authorization.split(" ")[1]  # Assumindo que o token vem no formato "Bearer seu_token"
    
    # Valide o token e obtenha o usuário
    usuario_data = validar_token(token)
    if usuario_data['id'] is None:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

    return usuario_data  # Retorna os dados do usuário

async def checar_autenticacao(request: Request, call_next):
    usuario = await obter_usuario_logado(request)
    request.state.usuario = usuario
    response = await call_next(request)
    if response.status_code == status.HTTP_307_TEMPORARY_REDIRECT:
        return response
    return response

async def checar_autorizacao(request: Request):
    usuario = request.state.usuario if hasattr(request.state, "usuario") else None
    area_do_usuario = request.url.path.startswith("/usuario")
    area_do_cliente = request.url.path.startswith("/cliente")
    area_do_vendedor = request.url.path.startswith("/vendedor")
    if (area_do_usuario or area_do_cliente or area_do_vendedor) and not usuario.perfil:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if area_do_cliente and usuario.perfil != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if area_do_vendedor and usuario.perfil != 2:
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
    payload = {
        "id": id,  # Adiciona o ID do usuário
        "nome": nome,
        "email": email,
        "perfil": perfil,
        "telefone": telefone,
        "exp": datetime.now() + timedelta(days=1)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def validar_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return {"id": None, "nome": None, "email": None, "perfil": 0, "telefone": None, "mensagem": "Token expirado"}
    except jwt.InvalidTokenError:
        return {"id": None, "nome": None, "email": None, "perfil": 0, "telefone": None, "mensagem": "Token inválido"}
    except Exception as e:
        return {"id": None, "nome": None, "email": None, "perfil": 0, "telefone": None, "mensagem": f"Erro: {e}"}
    
def criar_cookie_auth(response, token):
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value=token,
        max_age=1800,
        httponly=True,
        samesite="lax",
    )
    return response

def configurar_swagger_auth(app):
    app.openapi_schema = app.openapi()
    app.openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    app.openapi_schema["security"] = [{"BearerAuth": []}]
