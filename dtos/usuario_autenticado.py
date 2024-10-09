from dataclasses import dataclass
from typing import Optional

@dataclass
class UsuarioAutenticado:    
    id: int  # Adicione o ID do usuário
    nome: Optional[str] = None
    email: Optional[str] = None
    perfil: Optional[int] = None
    telefone: Optional[str] = None  # Adicionando o telefone como atributo opcional