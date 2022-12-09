from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from src.infra.sqlalchemy.config.database import get_db
from src.infra.providers import token_provider
from src.infra.sqlalchemy.repositorios.repositorio_usuario import RepositorioUsuario


oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


def obter_user_logado(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    erro = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Token inválido.'
        )

    try:
        email = token_provider.verificar_access_token(token)
    except JWTError:
        raise erro

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token inválido.'
        )

    usuario = RepositorioUsuario(db).obter_por_email(email)

    if not usuario:
        raise erro

    return usuario