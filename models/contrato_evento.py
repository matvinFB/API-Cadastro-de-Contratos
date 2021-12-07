from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database.banco import Base
import uuid

class contrato_evento_db(Base):
    __tablename__= 't_contrato_evento'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_criacao = Column(DateTime)
    data_atualizacao = Column(DateTime)
    contrato_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    estado_anterior = Column(String)
    estado_posterior = Column(String)