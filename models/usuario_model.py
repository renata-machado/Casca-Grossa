from dataclasses import dataclass
from datetime import date
from typing import Optional

from models.endereco_model import Endereco


@dataclass
class Usuario:
    id: Optional[int] = None
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    senha: Optional[str] = None
    perfil: Optional[int] = None
    id_endereco:Optional[int]= None