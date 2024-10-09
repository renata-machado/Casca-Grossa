from dataclasses import dataclass
from typing import Optional

@dataclass
class Categoria:
    nome: str  # Primeiro os campos obrigatórios
    id: Optional[int] = None  # Depois os opcionais com valores padrão
    descricao: Optional[str] = None
