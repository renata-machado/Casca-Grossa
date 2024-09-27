from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Usuario:
    id: Optional[int] = None
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    senha: Optional[str] = None
    tema: Optional[str] = None
    perfil: Optional[int] = None
    endereco_cep: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_complemento: Optional[str] = None
    endereco_endereco: Optional[str] = None
    endereco_cidade: Optional[str] = None
    endereco_uf: Optional[str] = None
