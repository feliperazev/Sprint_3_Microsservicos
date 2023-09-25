from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from model.m_atividade import Atividade
from model.m_relatorio import Relatorio
from flask import jsonify, make_response
import json



class Relatorio_Schema(BaseModel):
    """ Define como um novo registro de relatório diário a ser inserido deve ser representado
    """
    relatorio: str = "Descrição do relatório..."
    id_atividade: int = 1
    id_projeto: int = 4
    id_colaborador: int = 2
    horas_acumuladas: float = 3.5

class Relatorio_Edit_Schema(BaseModel):
    """Define como um relatorio a ser alterado deve ser 
    representado.
    """    
    relatorio_id: int = 1
    relatorio: str = "Nova descrição."  
    id_projeto: int = 1
    id_colaborador: int = 1
    horas_acumuladas: float = 4.8
    atividade_id: float = 2

class Relatorio_View_Schema(BaseModel):
    """Define como uma atividade será retornada.
    """
    
    id_relatorio : int = 1
    Relatorio : str = "Pintura do prédio A"
    data_registro: datetime =  datetime.now()
    id_projeto : int = 78
    id_colaborador : int = 5
    horas_acumuladas : float = 1.4

class Relatorio_Busca_Schema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id da atividade
    """
    relatorio_id : int = 0


class Colaborador_Relatorio_Del_Schema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id da atividade
    """
    id_colaborador : int = 0

class Relatorio_Del_Schema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    code: int


class Relatorios_Listagem_Schema(BaseModel):
    """ Define como uma listagem de atividades será retornada.
    """

    lista_relatorios : List[Relatorio_View_Schema]    

def apresenta_lista_relatorios(lista_relatorios: List[Relatorio]):
    
    """ Retorna uma representação de uma lista de atividades
        seguindo o schema definido em Atividade_View_Schema.
    """
    
    result = []
    for c in lista_relatorios:
        result.append(
            {
                {
                    "id_relatorio": c.id,
                    "data_registro": c.data_registro,
                    "relatorio": c.relatorio,
                    "id_projeto": c.id_projeto,
                    "id_colaborador": c.id_colaborador,
                    "horas_acumuladas": c.horas_acumuladas
                }
            }
        )
    data = json.load({"lista_relatorios": result})
    response = make_response(json.dump((data)))
    response.headers['Content-Type']="application/json"
    return response


def apresenta_relatorio(relatorio):
        """Retorna uma representação de um relatório seguindo
           o schema definido em Relatorio_View_Schema.
    """
        return {       
        "id": relatorio.relatorio,
        "data_registro": relatorio.data_registro,
        "relatorio": relatorio.relatorio,
        "id_projeto": relatorio.id_projeto,
        "id_colaborador": relatorio.id_colaborador,
        "horas_acumuladas":relatorio.horas_acumuladas
               
    }