from fastapi import APIRouter, status, Response
from controllers.contratoController import *
#IMPORT VALIDATION MODELS
from validation.models import *
#FIM IMPORT VALIDATION MODELS

#IMPORT MODELS
from models.cliente import cliente_db
from models.endereco import endereco_db
from models.ponto import ponto_db
from models.contrato import contrato_db
#FIM IMPORT MODELS

#IMPORT DATABASE
from database import *
from database.banco import session
#FIM IMPORT DATABASE
import datetime

router = APIRouter()

@router.post('/')
def post_ponto(ponto:Ponto):
    try:
        cliente = session.query(cliente_db).filter(cliente_db.id == ponto.cliente_id).first()
        endereco = session.query(endereco_db).filter(endereco_db.id == ponto.endereco_id).first()
        #checa se um dos dois tem data de remoção
        if (cliente and cliente.data_remocao != None) or (endereco and endereco.data_remocao != None):
            print("foi aqui")
            raise

        #checa se essa combinação já existe mas está desativada, se sim ativa, caso contrário responde status 400
        ponto_query = session.query(ponto_db).filter(ponto_db.cliente_id == ponto.cliente_id, ponto_db.endereco_id == ponto.endereco_id).first()

        if ponto_query and ponto_query.data_remocao:
            ponto_query.data_remocao = None
            session.add(ponto_query)
            session.commit() 
            return Response(status_code=status.HTTP_201_CREATED)
        
        elif ponto_query:
            raise 

        
        #caso usuário e endereço existam e não estejam em uso nem possam ser reativados cria ponto
        ponto = ponto_db(
            data_criacao = datetime.datetime.now(),
            cliente_id = ponto.cliente_id,
            endereco_id = ponto.endereco_id
        )

        session.add(ponto)
        session.commit()

        return Response(status_code=status.HTTP_201_CREATED)
        
    except:
        session.rollback()
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

@router.get('/')
def get_pontos(cliente_id = None, endereco_id = None):
    lista = []
    listaqueries = []
    try:
        if(cliente_id):
            listaqueries.append(ponto_db.cliente_id == cliente_id)

        if(endereco_id):
            listaqueries.append(ponto_db.endereco_id == endereco_id)

        queries = session.query(ponto_db).filter(*listaqueries, ponto_db.data_remocao == None) 

        for query in queries:
            cliente = session.query(cliente_db).filter(cliente_db.id == query.cliente_id).first()
            endereco = session.query(endereco_db).filter(endereco_db.id == query.endereco_id).first()
            
            lista.append({
                "id" : query.id,
                "cliente_id" : query.cliente_id,
                "cliente_nome" : cliente.nome,
                "cliente_tipo" : cliente.tipo,
                "endereco_id" : query.endereco_id,
                "endereco_logradouro" : endereco.logradouro, 
                "endereco_bairro" : endereco.bairro, 
                "endereco_numero" : endereco.numero})
        
        return {"dados":lista}
    except:
        session.rollback()
        return Response(status_code=status.HTTP_400_BAD_REQUEST) 



@router.delete('/{id}')
def delete_ponto(id):
    try:
        query = session.query(ponto_db).filter(ponto_db.id == id).first()
        #Se a query não tem data de remoção remove, caso contrário status 400
        if query.data_remocao == None:
            query.data_remocao = datetime.datetime.now()

            query_contratos = session.query(contrato_db).filter(contrato_db.ponto_id == id)
            for contrato in query_contratos:
                delete_contrato(contrato.id)
            session.add(query)
            session.commit()
        else:
            raise
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except:
        session.rollback()
        return Response(status_code=status.HTTP_400_BAD_REQUEST)