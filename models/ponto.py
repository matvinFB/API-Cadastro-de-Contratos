from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database.banco import Base
import uuid

class ponto_db(Base):
    
    __tablename__ = 't_ponto'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_criacao = Column(DateTime)
    data_atualizacao = Column(DateTime)
    data_remocao = Column(DateTime)
    cliente_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    endereco_id = Column(UUID(as_uuid=True), default=uuid.uuid4)