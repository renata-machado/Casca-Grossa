from dataclasses import dataclass
from typing import Optional

@dataclass
class Estoque:
    
    id_produtor: int
    id_produto: int
    quantidade: int
    id: Optional[int] = None