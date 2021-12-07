from fastapi import APIRouter, status, Response
from controllers.pontoController import *

#IMPORT VALIDATION MODELS
from validation.models import *
#FIM IMPORT VALIDATION MODELS

#IMPORT MODELS
from models.cliente import cliente_db
from models.ponto import ponto_db
#FIM IMPORT MODELS

#IMPORT DATABASE
from database import *
from database.banco import session
#FIM IMPORT DATABASE
import datetime


router = APIRouter()

@router.get("/")
def get_clientes(nome = None, tipo = None):
    lista = []
    listaqueries = []

    try:
        if(nome):
            listaqueries.append(cliente_db.nome == nome)
        if(tipo):
            listaqueries.append(cliente_db.tipo == tipo)

        query = session.query(cliente_db).filter(*listaqueries) 

        for i in query:
            if i.data_remocao:
                continue
            lista.append(Cliente(nome = i.nome, tipo=i.tipo))
        return {"dados":lista}
    except:
        session.rollback()
        return Response(status_code=status.HTTP_400_BAD_REQUEST) 

    

@router.post("/")
def post_cliente(cliente : Cliente): 
    try:
        query = session.query(cliente_db).filter(cliente_db.nome == cliente.nome).first()
        if query:
            if(query.data_remocao != None):
                query.data_atualizacao = datetime.datetime.now()
                query.data_remocao = None
                session.add(query)
                session.commit()
                return Response(status_code=status.HTTP_201_CREATED)
            else:
                raise
    except:
        pass

    try:
        user = cliente_db(
            id = None,
            nome = cliente.nome,
            data_criacao = datetime.datetime.now(),
            tipo = cliente.tipo
            )
    except:
        raise
    try:
        session.add(user)
        session.commit()
        return Response(status_code=status.HTTP_201_CREATED)
    except:
        session.rollback()
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

@router.put("/{id}")
def put_cliente(id, cliente : Cliente):
    try:
        query = session.query(cliente_db).filter(cliente_db.id == id).first()
        if query and query.data_remocao == None:
            query.nome = cliente.nome
            query.tipo = cliente.tipo
            query.data_atualizacao = datetime.datetime.now()
            session.add(query)
            session.commit()
        else:
            raise
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except:
        session.rollback()
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

@router.get("/{id}")
def get_cliente(id):
    try:
        query = session.query(cliente_db).filter(cliente_db.id == id).first()
        if query.data_remocao:
            raise
        return Cliente(nome = query.nome, tipo = query.tipo)
    except:
        session.rollback()
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

@router.delete("/{id}")
def delet_cliente(id):
    try:
        query = session.query(cliente_db).filter(cliente_db.id == id).first()
        if query and query.data_remocao == None:
            query.data_remocao = datetime.datetime.now()

            pontos_query = session.query(ponto_db).filter(ponto_db.cliente_id ==query.id)
            for ponto in pontos_query:
                delete_ponto(ponto.id)

            session.add(query)
            session.commit()
        else:
            raise
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except:
        session.rollback()
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
