from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session
from model.m_colaborador import Colaborador

import json

from schemas.sch_colaborador import *

from schemas.error import ErrorSchema
from flask_cors import CORS

import requests



info = Info(title="API Colaborador", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

#definindo tags
home_tag = Tag(name="Documentação API serviço Colaborador", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
colaborador_tag = Tag(name="Colaborador", description="Adição, visualização e remoção de registros à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/add_colaborador', tags=[colaborador_tag],
          responses={
              "200": Colaborador_View_Schema,
              "409": ErrorSchema,
              "400": ErrorSchema})
def add_colaborador(form:Colaborador_Schema):
    """Adiciona um novo registro de E1 à base de dados.
    """
    cep = str(form.cep)
    link = link = f'https://viacep.com.br/ws/{cep}/json/'
    requisicao = requests.get(link)
    dic_requisicao = requisicao.json()
        
    colaborador = Colaborador(
        nome=form.nome,
        idade=form.idade,
        cep=form.cep,
        logradouro = dic_requisicao['logradouro'],
        bairro=dic_requisicao['bairro'],
        cidade=dic_requisicao['localidade'],
        uf=dic_requisicao['uf'],
        )
        
    if requisicao.ok:

        try:
            session = Session()
            session.add(colaborador)
            session.commit()
            return apresenta_colaborador(colaborador), 200

        except IntegrityError as e:
            error_msg = "Erro! Registro de mesmo atributo 1 já salvo na base."
            return {"message": error_msg}, 409
        except Exception as e:
            error_msg = "Erro! Não foi possível salvar novo registro."
            return {"message": e}, 400
    else:
        error_msg = "Falha na consulta de CEP."
        return {"message": error_msg}, requisicao.status_code
    
@app.get('/busca_listagem_colaboradores', tags=[colaborador_tag],
         responses={
             "200": Colaborador_View_Schema,
              "409": ErrorSchema,
              "400": ErrorSchema})
def get_lista_colaboradores():
    """Faz a busca por todos os registros na tabela Colaborador,
       requisita ao serviço de controle de atividades as atividades cadastradas
       e retorna uma representação da listagem de colaboradores com suas respectivas atividades executadas."""

    link = 'http://servico_controle_atividades:5000/busca_listagem_atividades'

    requisicao = requests.get(link)
    json_atividades = requisicao.json()
    
    

    session = Session()
    colaboradores = session.query(Colaborador).all()

    session = Session()
    colaboradores = session.query(Colaborador).all()
    
    return apresenta_listagem_colaboradores(colaboradores=colaboradores, json_atividades=json_atividades), 200
        
                
@app.delete('/del_colaborador', tags=[colaborador_tag],
            responses={
             "200":Colaborador_Del_Schema,
             "404":ErrorSchema
             })
def del_colaborador(query: Colaborador_Busca_Schema):
    """Deleta um registro de colaborador a partir do id informado
    
       Retorna uma mensagem de confirmação de remoção.
    """

    registro_id = query.id_colaborador
    session = Session()
    count = session.query(Colaborador).filter(Colaborador.id == registro_id).delete()
    session.commit()

    if count == 1:
        error_msg = "Registro deletado!"
        link = f'http://localhost:5000/del_relatorios{registro_id}'
        requisicao = requests.get(link)
        return {"message": error_msg}, 200
    else:
        error_msg = "Registro de colaborador não encontrado na base."
        return {"message": error_msg}, 404 

        
