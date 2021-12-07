from fastapi import APIRouter, status, Response
from controllers.pontoController import *

#IMPORT VALIDATION MODELS
from validation.models import *
#FIM IMPORT VALIDATION MODELS

#IMPORT MODELS
from models.endereco import endereco_db
from models.ponto import ponto_db
#FIM IMPORT MODELS

#IMPORT DATABASE
from database import *
from database.banco import session
#FIM IMPORT DATABASE
import datetime

router = APIRouter()

@router.post("/")
def post_endereco(endereco : Endereco):
    try:
        query = session.query(endereco_db).filter(endereco_db.logradouro == endereco.logradouro, endereco_db.bairro == endereco.bairro, endereco_db.numero == endereco.numero).first()
        if(query.data_remocao != None):
            query.data_atualizacao = datetime.datetime.now()
            query.data_remocao = None
            session.add(query)
            session.commit()
            return Response(status_code=status.HTTP_201_CREATED)
        else:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)
    except:
        session.rollback()
        pass

    try:
        endereco = endereco_db(
        id = None,
        logradouro = endereco.logradouro,
        bairro = endereco.bairro,
        numero = endereco.numero,
        data_criacao = datetime.datetime.now(),
        )
        session.add(endereco)
        session.commit()
        return Response(status_code=status.HTTP_201_CREATED)
    except:
        session.rollback()
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

@router.get("/")
def get_enderecos(logradouro = None, bairro = None, numero = None):
    lista = []
    listaqueries = []
    try:

        if(logradouro):
            listaqueries.append(endereco_db.logradouro == logradouro)

        if(bairro):
            listaqueries.append(endereco_db.bairro == bairro)

        if(numero):
            listaqueries.append(endereco_db.numero == numero)
    
        query = session.query(endereco_db).filter(*listaqueries) 
  
        for i in query:
            if i.data_remocao:
                continue
            lista.append(Endereco(logradouro = i.logradouro, bairro=i.bairro, numero = i.numero))
        return {"dados":lista}
    except:
        session.rollback()
        return Response(status_code=status.HTTP_400_BAD_REQUEST) 

@router.put("/{id}")
def put_endereco(id, endereco : Endereco):
    
    try:
        query = session.query(endereco_db).filter(endereco_db.id == id).first()
        if query and query.data_remocao == None:
            query.logradouro = endereco.logradouro
            query.bairro = endereco.bairro
            query.numero = endereco.numero
            query.data_atualizacao = datetime.datetime.now()
            session.add(query)
            session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise
        
    except:
        session.rollback()
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

@router.get("/{id}")
def get_endereco(id):
    try:
        query = session.query(endereco_db).filter(endereco_db.id == id).first()
        if query.data_remocao:
            raise
        return Endereco(logradouro = query.logradouro, bairro = query.bairro, numero = query.numero)
    except:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

@router.delete("/{id}")
def delete_endereco(id):
    try:
        query = session.query(endereco_db).filter(endereco_db.id == id).first()
        #Se a query não tem data de remoção remove, caso contrário status 400
        if query.data_remocao == None:
            query.data_remocao = datetime.datetime.now()
            
            #acha todos os pontos que tenham esse endereço e os desativa
            pontos_query = session.query(ponto_db).filter(ponto_db.endereco_id ==query.id)
            for ponto in pontos_query:
                delete_ponto(ponto.id)
            
            #conclui a remoção do endereço
            session.add(query)
            session.commit()
            
        else:
            raise
    
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except:
        session.rollback()
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
