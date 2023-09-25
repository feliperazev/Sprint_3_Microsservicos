from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union    

from model import Base
from model.m_relatorio import Relatorio

class Atividade(Base):
    __tablename__ = 'tb_atividades'

    atividade_id = Column(Integer, primary_key=True)
    descricao = Column(String(150))
    relatorios = relationship("Relatorio", cascade = 'all, delete-orphan')
    
    def __init__(self, descricao):
        self.descricao = descricao
    
    def add_relatorio_diario(self, relatorio: Relatorio):
        self.relatorios.append(relatorio)
    

    