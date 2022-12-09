from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.infra.sqlalchemy.config.database import Base


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    nome = Column(String)
    senha = Column(String)
    telefone = Column(String)