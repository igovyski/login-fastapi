from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session

from src.schemas import schemas
from src.infra.sqlalchemy.repositorios.repositorio_usuario import *
from src.infra.sqlalchemy.config.database import get_db
from src.infra.providers import hash_provider, token_provider
from src.routes.auth_utils import obter_user_logado


router = APIRouter()

# Rotas Usuários
@router.post('/signup', response_model=schemas.UsuarioSimples, status_code=status.HTTP_201_CREATED)
def signup(usuario: schemas.Usuario, db: Session = Depends(get_db)):
    # Verificar se usuário já existe
    usuario_localizado = RepositorioUsuario(db).obter_por_email(usuario.email)

    if usuario_localizado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Já existe um usuário com este email.'
        )
    
    # Criar usuário
    usuario.senha = hash_provider.gerar_hash(usuario.senha)
    usuario_criado = RepositorioUsuario(db).criar(usuario)
    return usuario_criado

@router.post('/token', status_code=status.HTTP_200_OK)
def login(login_data: schemas.LoginData, db: Session = Depends(get_db)):
    email = login_data.email
    senha = login_data.senha

    usuario = RepositorioUsuario(db).obter_por_email(email)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email ou senha incorretos.'
        )

    senha_valida = hash_provider.verificar_hash(senha, usuario.senha)

    if not senha_valida:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email ou senha incorretos.'
        )

    # Gerar Token JWT
    token = token_provider.criar_access_token({'sub': usuario.email})

    return schemas.LoginSucesso(usuario=usuario, access_token=token)


@router.get('/me', response_model=schemas.UsuarioSimples, status_code=status.HTTP_200_OK)
def me(usuario: schemas.Usuario = Depends(obter_user_logado)):
    return usuario