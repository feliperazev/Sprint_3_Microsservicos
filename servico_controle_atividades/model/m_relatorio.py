from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base


class Relatorio(Base):
    __tablename__ = 'tb_relatorios'

    id = Column(Integer, primary_key=True)
    relatorio = Column(String, default=str(id))
    data_registro =  Column(DateTime, default=datetime.now())
    id_projeto = Column(Integer)
    id_colaborador = Column(Integer)
    horas_acumuladas = Column(Float)
    
    atividade_id = Column(Integer, ForeignKey('tb_atividades.atividade_id', ondelete='CASCADE'))
    


    def __init__(self, relatorio, id_projeto, id_colaborador, horas_acumuladas):

        self.relatorio = relatorio
        self.id_projeto = id_projeto
        self.id_colaborador = id_colaborador
        self.horas_acumuladas = horas_acumuladas

