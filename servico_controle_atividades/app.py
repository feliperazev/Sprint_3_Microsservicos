from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, jsonify
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session
from model.m_atividade import Atividade
from model.m_relatorio import Relatorio

from schemas.sch_atividade import *
from schemas.sch_relatorio import *
from schemas.sch_error import ErrorSchema
from flask_cors import CORS



info = Info(title="API Controle de Atividades", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

#definindo tags
home_tag = Tag(name="Documentação API Controle de Atividades", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
atividade_tag = Tag(name="Atividade", description="Adição, visualização e remoção de registros à base")
relatorio_tag = Tag(name="Relatório", description="Adição, visualização e remoção de registros à base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/add_atividade', tags=[atividade_tag],
          responses={
              "200": Atividade_View_Schema,
              "409": ErrorSchema,
              "400": ErrorSchema})
def add_atividade(form:Atividade_Schema):
    """Adiciona um nova atividade à base de dados.
    """
    atividade = Atividade(descricao=form.descricao)
    
    try:
        session = Session()
        session.add(atividade)
        session.commit()
        return apresenta_atividade(atividade), 200
    except IntegrityError as e:
        error_msg = "Erro! Atividade de mesma descrição já salva na base."
        return {"message": error_msg}, 409
    except Exception as e:
        return {"message": e}, 400


@app.post('/add_relatorio_diario', tags=[relatorio_tag],
            responses={
             "200":Relatorio_Schema,
             "404":ErrorSchema}          
          )
def add_relatorio_diario(form: Relatorio_Schema):
    """Adiciona um novo relatorio diario,
       relacionado à tabela de atividades pelo id de uma atividade.

       Retorna uma representação dos relatórios diários e atividades associados. 
    """

    id_atividade = form.id_atividade
    
    try:
        
        session = Session()
        atividade = session.query(Atividade).filter(Atividade.atividade_id == id_atividade).first()

        if not atividade:
            error_msg = "Atividade não encontrada na base de dados."
            return {"message": error_msg}, 404
        id_projeto = form.id_projeto
        id_colaborador = form.id_colaborador
        horas_acumuladas = form.horas_acumuladas
        relatorio = form.relatorio
        relatorio_diario = Relatorio(relatorio=relatorio, id_projeto=id_projeto,id_colaborador=id_colaborador, horas_acumuladas=horas_acumuladas)
        atividade.add_relatorio_diario(relatorio_diario)
        session.commit()

        return apresenta_atividade(atividade), 200
    except Exception as e:
        error_msg = "Não foi possível salvar novo item.. :/"
        return{"message": error_msg}, 400

@app.get('/busca_atividade', tags=[atividade_tag],
         responses={
             "200":Atividade_View_Schema,
             "404":ErrorSchema
             })
def get_atividade(query: Atividade_Busca_Schema):
    """Faz a busca por um registro na tabela Atividade a partir do id"""

    atividade_id = query.atividade_id
    session = Session()
    atividade = session.query(Atividade).filter(Atividade.atividade_id == atividade_id).first()
        
    if not atividade:
        error_msg = "Atividade não encontrada"
        return {"message": error_msg}, 404
    else:
         return apresenta_atividade(atividade)

@app.get('/busca_listagem_atividades', tags=[atividade_tag],
         responses={
             "200": Atividade_Listagem_Schema,
              "409": ErrorSchema,
              "400": ErrorSchema})
def get_lista_atividades():
    """Faz a busca por todas as atividades na tabela Atividades e retorna uma representação da listagem desses registros"""
    session = Session()
    atividades = session.query(Atividade).all()

    if not atividades:
        return {"lista_atividades":[]}, 200
    else:
        return apresenta_lista_atividades(atividades), 200
        

@app.delete('/del_atividade', tags=[atividade_tag],
            responses={
             "200":Atividade_Del_Schema,
             "404":ErrorSchema
             })
def del_atividade(query: Atividade_Busca_Schema):
    """Deleta um registro a partir do id informado
    
       Retorna uma mensagem de confirmação de remoção.
    """

    atividade_id = query.atividade_id
    session = Session()
    atividade = session.query(Atividade).filter(Atividade.atividade_id == atividade_id).first()
    
    session.delete(atividade)
    session.commit()
    
    if atividade:
        error_msg = "Atividade deletada!"
        return {"message": error_msg}, 200
    else:
        error_msg = "Atividade não encontrada..."
        return {"message": error_msg}, 404 
    


@app.delete('/del_relatorios', tags=[relatorio_tag],
            responses={
             "200":Relatorio_Del_Schema,
             "404":ErrorSchema
             })
def del_relatorios(query: Colaborador_Relatorio_Del_Schema):
    """Deleta os registros dos relatórios a partir do id do colaborador informado
    
       Retorna uma mensagem de confirmação de remoção.
    """

    id_colaborador = query.id_colaborador
    session = Session()
    relatorios = session.query(Relatorio).filter(Relatorio.id_colaborador == id_colaborador).all()
    
    session.delete(relatorios)
    session.commit()
    
    if relatorios:
        error_msg = "Relatorio deletado!"
        return {"message": error_msg}, 200
    else:
        error_msg = "Relatorio não encontrado..."
        return {"message": error_msg}, 404 

@app.put('/alter_atividade', tags=[atividade_tag],
        responses={"200": Atividade_Busca_Schema, "409": ErrorSchema, "400": ErrorSchema})
def edit_atividade(form: Atividade_Edit_Schema):
    
    """Edita uma atividade de acordo com o id informado"""
    
    nova_atividade = Atividade(descricao=form.descricao)
    nova_atividade.atividade_id = form.atividade_id
    try:
        session = Session()
        session.query(Atividade).filter(Atividade.atividade_id == form.atividade_id).update(
            {
                "descricao": form.descricao
            }, synchronize_session="fetch"
        )
        session.commit()
        
        return apresenta_atividade(nova_atividade), 200
    except IntegrityError as e:
        error_msg = e
        return {"message": error_msg}, 409
    except Exception as e:
        error_msg = e
        return {"message": error_msg}, 400

@app.put('/alter_relatorio', tags=[relatorio_tag],
        responses={"200": Relatorio_Busca_Schema, "409": ErrorSchema, "400": ErrorSchema})
def edit_relatorio(form: Relatorio_Edit_Schema):
    
    """Edita um relatorio de acordo com o id informado"""
    
    novo_relatorio = Relatorio(
                                
                relatorio=form.relatorio,
                id_projeto=form.id_projeto,
                id_colaborador=form.id_colaborador,
                horas_acumuladas=form.horas_acumuladas,


                
                )
    novo_relatorio.id = form.relatorio_id
    novo_relatorio.atividade_id = form.atividade_id
    novo_relatorio.data_registro = datetime.now()
    try:
        session = Session()
        session.query(Relatorio).filter(Relatorio.id == form.relatorio_id).update(
            {
                "relatorio": form.relatorio,
                "id_projeto": form.id_projeto,
                "id_colaborador":form.id_colaborador,
                "horas_acumuladas":form.horas_acumuladas,
                "atividade_id":form.atividade_id,
                "data_registro":novo_relatorio.data_registro

            }, synchronize_session="fetch"
        )
        session.commit()
        
        return apresenta_relatorio(novo_relatorio), 200
    except IntegrityError as e:
        error_msg = e
        return {"message": error_msg}, 409
    except Exception as e:
        error_msg = e
        return {"message": error_msg}, 400

@app.get('/busca_relatorio', tags=[relatorio_tag],
         responses={
             "200":Relatorio_View_Schema,
             "404":ErrorSchema
             })
def get_relatorio(query: Relatorio_Busca_Schema):
    """Faz a busca por um registro na tabela Atividade a partir do id"""

    relatorio_id = query.relatorio_id
    session = Session()
    relatorio = session.query(Relatorio).filter(Relatorio.id == relatorio_id).first()
        
    if not relatorio:
        error_msg = "Relatório não encontrado!"
        return {"message": error_msg}, 404
    else:
         return apresenta_relatorio(relatorio)


@app.get('/busca_listagem_relatorios', tags=[relatorio_tag],
         responses={
             "200": Relatorios_Listagem_Schema,
              "409": ErrorSchema,
              "400": ErrorSchema})
def get_lista_relatorios():
    """Faz a busca por todos os relatórios na tabela Relatorios e retorna uma representação da listagem desses registros"""
    session = Session()
    relatorios = session.query(Relatorio).all()

    if not (relatorios):
        return {"lista_relatorios":[]}, 200
    else:
        return apresenta_lista_atividades (relatorios), 200