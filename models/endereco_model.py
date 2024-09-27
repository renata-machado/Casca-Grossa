from dataclasses import dataclass
from typing import Optional


@dataclass
class Endereco:
    endereco_cep: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_complemento: Optional[str] = None
    endereco_bairro: Optional[str] = None
    endereco_cidade: Optional[str] = None
    endereco_uf: Optional[str] = None  
    id_usuario: Optional[str] = None