from pydantic import BaseModel
from typing import Optional, List


class Usuario(BaseModel):
    id: Optional[int] = None
    email: str
    nome: str
    senha: str
    telefone: str

    class Config:
        orm_mode = True


class UsuarioSimples(BaseModel):
    id: Optional[int] = None
    email: str
    nome: str
    telefone: str
    
    class Config:
        orm_mode = True


class LoginData(BaseModel):
    email: str
    senha: str


class LoginSucesso(BaseModel):
    usuario: UsuarioSimples
    access_token: str