from fastapi import APIRouter, status, Response
from sqlalchemy import asc

#IMPORT MODELS
from models.contrato_evento import contrato_evento_db
#FIM IMPORT MODELS

#IMPORT DATABASE
from database import *
from database.banco import session
#FIM IMPORT DATABASE

router = APIRouter()

@router.get('/{id}/historico')
def get_historico(id):
    try:
        queries = session.query(contrato_evento_db).filter(contrato_evento_db.contrato_id == id).order_by(asc(contrato_evento_db.data_criacao))
        lista = []

        for evento in queries:
            lista.append({
                "id": evento.contrato_id,
                "data_evento": evento.data_criacao,
                "estado_antigo": evento.estado_anterior, 
                "estado_novo": evento.estado_posterior
            })
        
        return {"dados" : lista}
    
    except:
        session.rollback()
        return Response(status_code=status.HTTP_400_BAD_REQUEST)