from fastapi import APIRouter, status, Response
from sqlalchemy import asc

#IMPORT VALIDATION MODELS
from validation.models import *
#FIM IMPORT VALIDATION MODELS

#IMPORT MODELS
from models.cliente import cliente_db
from models.endereco import endereco_db
from models.ponto import ponto_db
from models.contrato import contrato_db
from models.contrato_evento import contrato_evento_db
#FIM IMPORT MODELS

#IMPORT DATABASE
from database import *
from database.banco import session
#FIM IMPORT DATABASE
import datetime


router = APIRouter()
@router.post('/')
def post_contrato(contrato : Contrato):
    try:
        contrato = session.query(contrato_db).filter(contrato_db.ponto_id == contrato.ponto_id, contrato_db.estado != "Cancelado").first()

        if contrato:
            print(contrato)
            if contrato.data_remocao:
                raise
            
            estado = contrato.estado
            if contrato.estado == 'Desativado Temporario':
                contrato.data_atualizacao = datetime.datetime.now()
                contrato.estado = 'Em vigor'

            session.add(contrato)
            session.commit()

            #Após a alteração do contrato cria o evento
            contrato_evento = contrato_evento_db (
                    data_criacao = datetime.datetime.now(),
                    contrato_id = contrato.id,
                    estado_anterior = estado,
                    estado_posterior = 'Em vigor'
                )

            session.add(contrato_evento)
            session.commit()

            return Response(status_code=status.HTTP_201_CREATED)

        contrato = contrato_db(
            data_criacao = datetime.datetime.now(),
            ponto_id = contrato.ponto_id,
            estado = 'Em vigor'
        )

        session.add(contrato)
        session.commit()
        return Response(status_code=status.HTTP_201_CREATED)
    except:
        session.rollback()
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

@router.get('/')
def get_contratos(cliente_id = None, endereco_id = None):
    
    lista = []
    lista_queries = []
    if cliente_id:
        lista_queries.append(ponto_db.cliente_id == cliente_id)
    if endereco_id:
        lista_queries.append(ponto_db.endereco_id == endereco_id)

    queries = session.query(contrato_db.id,ponto_db.cliente_id, ponto_db.endereco_id).join(ponto_db, contrato_db.ponto_id == ponto_db.id).filter(*lista_queries, contrato_db.data_remocao == None)
    try:
        if queries:
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
        else:
            raise
    except:
        session.rollback()
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

@router.get('/{id}')
def get_contratos(id):
    try:
        contrato = session.query(contrato_db).filter(contrato_db.id == id).first()
        ponto = session.query(ponto_db).filter(ponto_db.id == contrato.ponto_id).first()
        if contrato:
            cliente = session.query(cliente_db).filter(cliente_db.id == ponto.cliente_id).first()
            endereco = session.query(endereco_db).filter(endereco_db.id == ponto.endereco_id).first()
            
            return({
                "id" : contrato.id,
                "cliente_id" : ponto.cliente_id,
                "cliente_nome" : cliente.nome,
                "cliente_tipo" : cliente.tipo,
                "endereco_id" : ponto.endereco_id,
                "endereco_logradouro" : endereco.logradouro, 
                "endereco_bairro" : endereco.bairro, 
                "endereco_numero" : endereco.numero})
    except:
        session.rollback()
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

@router.delete('/{id}')
def delete_contrato(id):
    try:
        contrato = session.query(contrato_db).filter(contrato_db.id == id).first()
        if contrato.data_remocao == None:
            estado = contrato.estado

            if contrato.estado == 'Em vigor':

                contrato.estado = 'Desativado Temporario'

            elif contrato.estado == 'Desativado Temporario':
                contrato.data_remocao = datetime.datetime.now()
                contrato.estado = 'Cancelado'
            else:
                raise
                
            session.add(contrato)
            session.commit()

            #Após a atualização do contrato cria o evento do contrato
            contrato_evento = contrato_evento_db(
                    data_criacao = datetime.datetime.now(),
                    contrato_id = contrato.id,
                    estado_anterior = estado,
                    estado_posterior = contrato.estado
                )
                
            session.add(contrato_evento)
            session.commit()


        else:
            raise
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except:
        session.rollback()
        return Response(status_code=status.HTTP_400_BAD_REQUEST)



