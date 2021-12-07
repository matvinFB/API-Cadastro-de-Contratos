from pydantic import BaseModel
from uuid import UUID

class Cliente(BaseModel):
    nome : str
    tipo : str

class Endereco(BaseModel):
    logradouro : str
    bairro : str
    numero : int

class Ponto(BaseModel):
    cliente_id: UUID
    endereco_id : UUID

class Contrato(BaseModel):
    ponto_id : UUID
    


