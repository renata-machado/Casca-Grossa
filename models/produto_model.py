from dataclasses import dataclass
from typing import Optional

@dataclass
class Produto:
    id: Optional[int] = None
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    quantidade: Optional[int] = None
    id_categoria: Optional[int] = None
