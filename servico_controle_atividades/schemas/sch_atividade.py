from pydantic import BaseModel
from typing import Optional, List
from model.m_atividade import Atividade
from model.m_relatorio import Relatorio
from flask import jsonify, make_response

from schemas.sch_relatorio import *

class Atividade_Schema(BaseModel):
    """Define como uma nova atividade a ser inserida deve ser 
    representada.
    """
    descricao: str = "Pintura"
class Atividade_Edit_Schema(BaseModel):
    """Define como uma atividade a ser alterada deve ser 
    representada.
    """
    atividade_id: int = 1
    descricao: str = "Nova descrição."    
class Atividade_Busca_Schema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id da atividade
    """
    atividade_id : int = 0
    
class Atividade_View_Schema(BaseModel):
    """Define como uma atividade será retornada.
    """
    
    id_atividade : int = 1
    descricao : str = "Pintura"
    lista_relatorios : List[Relatorio_Schema]
        
class Atividade_Listagem_Schema(BaseModel):
    """ Define como uma listagem de atividades será retornada.
    """

    lista_atividades : List[Atividade_View_Schema]    

class Atividade_Del_Schema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    code: int
    
def apresenta_lista_atividades(lista_atividades: List[Atividade]):
    
    """ Retorna uma representação de uma lista de atividades
        seguindo o schema definido em Atividade_View_Schema.
    """
    
    result = []
    for atividade in lista_atividades:
        result.append(
            {
                "id": atividade.atividade_id,
                "descricao": atividade.descricao,
                "lista_relatorios":[
                                      {
                                       "id_relatorio": c.id,
                                       "data_registro": c.data_registro,
                                       "relatorio": c.relatorio,
                                       "id_projeto": c.id_projeto,
                                       "id_colaborador": c.id_colaborador,
                                       "horas_acumuladas": c.horas_acumuladas}
                                        
                                        for c in atividade.relatorios]
            }
        )
    return jsonify({"lista_atividades": result})

def apresenta_atividade(atividade):
    """Retorna uma representação de uma atividade seguindo
       o schema definido em Atividade_View_Schema.
    """
    
    return jsonify({
        "id": atividade.atividade_id,
                "descricao": atividade.descricao,
                "lista_relatorios":[
                                      {
                                       "id_relatorio": c.id,
                                       "data_registro": c.data_registro,
                                       "relatorio": c.relatorio,
                                       "id_projeto": c.id_projeto,
                                       "id_colaborador": c.id_colaborador,
                                       "horas_acumuladas": c.horas_acumuladas}
                                        
                                        for c in atividade.relatorios]
    })
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


