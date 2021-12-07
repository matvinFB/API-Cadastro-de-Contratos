from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database.banco import Base
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