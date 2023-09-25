from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base


class Colaborador(Base):
    __tablename__ = 'tb_colaborador'

    id = Column("id_pk_colaborador", Integer, primary_key=True)
    nome = Column(String(150))
    idade = Column(Integer)
    cep = Column(Integer)
    logradouro = Column(String(150))
    bairro = Column(String(150))
    cidade = Column(String(150))
    uf = Column(String(150))

    
    
    def __init__(self, nome, idade, cep, logradouro, bairro, cidade, uf):
    
        
        self.nome = nome
        self.idade = idade
        self.cep = cep
        self.logradouro = logradouro
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf
        self.lista_atividades = []
        
    def add_atividade(self, atividade):
        self.lista_atividades.append(atividade)
        

    