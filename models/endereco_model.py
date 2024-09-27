from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Endereco:
    id: Optional[int] = None
    id_usuario: Optional[int] = None
    endereco_cep: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_complemento: Optional[str] = None
    endereco_endereco: Optional[str] = None
    endereco_cidade: Optional[str] = None
    endereco_uf: Optional[str] = None
