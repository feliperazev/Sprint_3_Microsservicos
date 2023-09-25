from pydantic import BaseModel
from typing import Optional, List
from model.m_colaborador import Colaborador
from datetime import datetime

class Colaborador_Schema(BaseModel):
    """Define como um novo registro de colaborador a ser inserido deve ser 
    representado.
    """
    nome: str = "João"
    idade: int = "20"
    cep: int = 28085130

class Colaborador_Busca_Schema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do colaborador.
    """
    id_colaborador: int = 0 

class Atividade_View_Schema(BaseModel):
    data_registro: str = datetime.now()
    id_colaborador: int = 1
    atividade: str = "Pintura."
    relatorio: str = "Atividade realizada no prédia A."

class Colaborador_View_Schema(BaseModel):
    """Define como um registro de um colaborador será retornado.
    """
    id_colaborador: int = 1
    nome: str = "João"
    idade: int = "20"
    cep: int = 28085130
    logradouro: str = "Rua do Passeio"
    bairro: str = "Centro"
    cidade: str = "Rio de Janeiro"
    uf: str = "RJ"
    lista_atividades: List[Atividade_View_Schema]

class Colaborador_Lista_Schema(BaseModel):
    """ Define como uma listagem de colaboradores será retornada.
    """

    lista_colaboradores: List[Colaborador_View_Schema]

class Colaborador_Del_Schema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    code: int

def apresenta_listagem_colaboradores(colaboradores, json_atividades):
    
    """ Retorna uma representação de uma lista de registros da entidade E1 
        seguindo o schema definido em Colaborador_View_Schema.
    """
    
    result = []
    for colaborador in  colaboradores:
        colaborador.lista_atividades = []
        for atividade in json_atividades["lista_atividades"]:
            for relatorio in atividade["lista_relatorios"]:
                if relatorio["id_colaborador"] == colaborador.id:
                    colaborador.add_atividade([relatorio['data_registro'],colaborador.id, atividade['descricao'], relatorio['relatorio']])
        result.append(
            {
            "id": colaborador.id,
            "nome": colaborador.nome,
            "idade": colaborador.idade,
            "cep": colaborador.cep,
            "logradouro": colaborador.logradouro,
            "bairro": colaborador.bairro,
            "cidade": colaborador.cidade,
            "uf": colaborador.uf,
            "lista_atividades": colaborador.lista_atividades
            }
        )
    return {"lista de colaboradores": result}

def apresenta_colaborador(colaborador: Colaborador):
    """Retorna uma representação de um registro de colaborador seguindo
       o schema definido em Colaborador_View_Schema.
    """
    return {
            "id": colaborador.id,
            "nome": colaborador.nome,
            "idade": colaborador.idade,
            "cep": colaborador.cep,
            "logradouro": colaborador.logradouro,
            "bairro": colaborador.bairro,
            "cidade": colaborador.cidade,
            "uf": colaborador.uf,
            
            "lista_atividades": [{"id da atividade": item.id, "atividade": item.atividade} for item in colaborador.lista_atividades]
    }