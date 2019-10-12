import pandas as pd
from sqlalchemy.engine import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, TIMESTAMP, FLOAT, Sequence, BOOLEAN, select
import json
import psycopg2
from postgres import Postgres


class buscar_dados:
    def __init__(self):
        self.engine = create_engine("postgresql+psycopg2://postgres:Meteoro585@localhost:5432/tcc")
        self.metadata = MetaData(self.engine)
        self.Cliente = Table('cliente', self.metadata,
                             Column('id', Integer, Sequence('cliente_id_seq'), primary_key=True),
                             Column('nome', String(9)),
                             Column('cep', String(9)),
                             Column('cpf', String(14)),
                             Column('idade', TIMESTAMP),
                             Column('sexo', String(1)),
                             Column('altura', FLOAT),
                             Column('peso', Integer),
                             Column('slario', Integer),
                             Column('dependentes', BOOLEAN),
                             Column('exercicios', Integer),
                             Column('dependentes', BOOLEAN),
                             Column('risco_cancer', FLOAT),
                             Column('dependentes', BOOLEAN),
                             Column('risco', String(1)),
                             )

    def criar_cliente(self):
        self.metadata.create_all()

    def conectar_BD(self):
        conn = self.engine.connect()
        return conn

    def buscar_dados_cliente(self, cpf):
        valor = select([self.Cliente.c.nome, self.Cliente.c.cpf, self.Cliente.c.slario, self.Cliente.c.risco])
        print(valor)
        row = self.conectar_BD().execute(valor).fetchone()
        return row


class json_transformar:
    def __init__(self):
        self.db = buscar_dados()

    def passar_cliente_json(self, cpf):
        cliente = self.db.buscar_dados_cliente(cpf)
        dic_cl = {"nome": cliente[0], "cpf": cliente[1], "salario": cliente[2], "risco": cliente[3]}
        return dic_cl


if __name__ == '__main__':
    pass
