from sqlalchemy.orm import Session
from sqlalchemy import select

from src.schemas import schemas
from src.infra.sqlalchemy.models import models

class RepositorioUsuario():


    def __init__(self, db: Session):
        self.db = db

    def criar(self, usuario: schemas.Usuario):
        db_usuario = models.Usuario(email = usuario.email,
                                    nome = usuario.nome,
                                    senha = usuario.senha,
                                    telefone = usuario.telefone)
        self.db.add(db_usuario)
        self.db.commit()
        self.db.refresh(db_usuario)

        return db_usuario

    def listar(self):
        stmt = select(models.Usuario)
        usuarios = self.db.execute(stmt).scalars().all()

        return usuarios

    def obter_por_email(self, email: str):
        stmt = select(models.Usuario) \
            .where(models.Usuario.email == email)

        return self.db.execute(stmt).scalars().first()

    def remover(self):
        pass