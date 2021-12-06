import sqlalchemy
from sqlalchemy.engine import base

from banco import Base
from banco import Base
from sqlalchemy import Column, String, DateTime, Date, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import UUIDType
import uuid

class cliente_db(Base):
    __tablename__ = 't_cliente'
    
    #id = Column(UUIDType, primary_key=True,  default=uuid.uuid4)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_criacao = Column(DateTime)
    data_atualizacao = Column(DateTime)
    nome = Column(String)
    data_remocao = Column(DateTime)
    tipo = Column(String)

    def __repr__ (self):
        return f'nome:{self.nome}, tipo: {self.tipo}'

class endereco_db(Base):
    __tablename__ = 't_endereco'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_criacao = Column(DateTime)
    data_atualizacao = Column(DateTime)
    logradouro = Column(String)
    bairro = Column(String)
    numero = Column(Integer)
    data_remocao = Column(DateTime)

class ponto_db(Base):
    
    __tablename__ = 't_ponto'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_criacao = Column(DateTime)
    data_atualizacao = Column(DateTime)
    data_remocao = Column(DateTime)
    cliente_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    endereco_id = Column(UUID(as_uuid=True), default=uuid.uuid4)

class contrato_db(Base):
    __tablename__= 't_contrato'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_criacao = Column(DateTime)
    data_atualizacao = Column(DateTime)
    data_remocao = Column(DateTime)
    ponto_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    estado = Column(String)

class contrato_evento_db(Base):
    __tablename__= 't_contrato_evento'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_criacao = Column(DateTime)
    data_atualizacao = Column(DateTime)
    contrato_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    estado_anterior = Column(String)
    estado_posterior = Column(String)


