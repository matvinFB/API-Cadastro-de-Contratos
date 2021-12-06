from fastapi import FastAPI, status, Response
from fastapi.responses import PlainTextResponse 
from fastapi.exceptions import RequestValidationError
from sqlalchemy import asc
from models import *
from dbmodels import *
from banco import session

import datetime



lista_clientes =  []

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handle(request, exc):
    return PlainTextResponse(status_code=400)

#CLIENTES
@app.get("/api/v1/clientes")
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

    

@app.post("/api/v1/clientes")
def post_cliente(cliente : Cliente): 
    try:
        query = session.query(cliente_db).filter(cliente_db.nome == user.nome).first()
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

@app.put("/api/v1/clientes/{id}")
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

@app.get("/api/v1/clientes/{id}")
def get_cliente(id):
    try:
        query = session.query(cliente_db).filter(cliente_db.id == id).first()
        if query.data_remocao:
            raise
        return Cliente(nome = query.nome, tipo = query.tipo)
    except:
        session.rollback()
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

@app.delete("/api/v1/clientes/{id}")
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

#FIM CLIENTES

#ENDEREÇOS 
@app.post("/api/v1/enderecos")
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

@app.get("/api/v1/enderecos")
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

@app.put("/api/v1/enderecos/{id}")
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

@app.get("/api/v1/enderecos/{id}")
def get_endereco(id):
    try:
        query = session.query(endereco_db).filter(endereco_db.id == id).first()
        if query.data_remocao:
            raise
        return Endereco(logradouro = query.logradouro, bairro = query.bairro, numero = query.numero)
    except:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

@app.delete("/api/v1/enderecos/{id}")
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

#FIM ENDEREÇOS

#PONTO
@app.post('/api/v1/pontos')
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

@app.get('/api/v1/pontos')
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



@app.delete('/api/v1/pontos/{id}')
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
#FIM PONTO

#CONTRATOS

@app.post('/api/v1/contratos')
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

@app.get('/api/v1/contratos')
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

@app.get('/api/v1/contratos/{id}')
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

@app.delete('/api/v1/contratos/{id}')
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


#FIM CONTRATOS

#HISTORICO
@app.get('/api/v1/contrato/{id}/historico')
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
#FIM HISTORICO