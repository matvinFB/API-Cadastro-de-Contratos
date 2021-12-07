from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from database.banco import Base
import uuid

class endereco_db(Base):
    __tablename__ = 't_endereco'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_criacao = Column(DateTime)
    data_atualizacao = Column(DateTime)
    logradouro = Column(String)
    bairro = Column(String)
    numero = Column(Integer)
    data_remocao = Column(DateTime)