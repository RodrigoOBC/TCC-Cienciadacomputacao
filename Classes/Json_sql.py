import pandas as pd
from sqlalchemy.engine import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, TIMESTAMP, FLOAT, Sequence, BOOLEAN, select
import json
import psycopg2
from postgres import Postgres
from .Cliente import Cliente


class buscar_dados:
    def __init__(self):
        self.engine = create_engine("postgresql+psycopg2://postgres:Meteoro585@localhost:5432/tcc")
        self.metadata = MetaData(self.engine)
        self.Cliente = Table('cliente', self.metadata,
                             Column('id', Integer, Sequence('cliente_id_seq'), primary_key=True),
                             Column('nome', String(50)),
                             Column('cep', String(10)),
                             Column('cpf', String(14)),
                             Column('idade', TIMESTAMP),
                             Column('sexo', String(1)),
                             Column('altura', FLOAT),
                             Column('peso', Integer),
                             Column('slario', Integer),
                             Column('dependentes', BOOLEAN),
                             Column('exercicios', Integer),
                             Column('risco_cancer', FLOAT),
                             Column('risco', String(1)),
                             )
        self.Funcionario = Table('Funcionario', self.metadata,
                                 Column('id_login', Integer, primary_key=True),
                                 Column('cpf', String(9)),
                                 Column('senha', String(33)),
                                 Column('nome', String(120)),
                                 Column('permicao', String(20)),
                                 Column('email', String(120)),

                                 )

    def criar_cliente(self):
        self.metadata.create_all()

    def conectar_BD(self):
        conn = self.engine.connect()
        return conn

    def buscar_dados_cliente(self, cpf):
        valor = select([self.Cliente.c.nome, self.Cliente.c.cpf, self.Cliente.c.slario, self.Cliente.c.risco]).where(
            self.Cliente.c.cpf == cpf)
        row = self.conectar_BD().execute(valor).fetchone()
        return row

    def inseri_funcionario(self, valor):

        self.Funcionario.insert().values(cpf=valor[0], senha=valor[1], nome=valor[2], permicao=valor[3],
                                         email=valor[4]).execute()

    def inserir_cliente(self, valor):
        try:
            self.Cliente.insert().values(cpf=valor[0], nome=valor[1], cep=valor[2], idade=valor[3], sexo=valor[4],
                                         altura=valor[5],
                                         peso=valor[6], slario=valor[7], dependentes=valor[8], exercicios=valor[9],
                                         risco_cancer=valor[10],
                                         risco=valor[11]).execute()
            return True
        except:
            return False


class json_transformar:
    def __init__(self):
        self.db = buscar_dados()

    def passar_cliente_json(self, cpf):
        cliente = self.db.buscar_dados_cliente(cpf)
        valor = cliente[2] * 36
        range_valor = False
        x = 10000
        if cliente[3] != 'N':
            while (range_valor == False):
                if valor <= x:
                    range_valor = True
                else:
                    x += 10000

            valor = (x, x / 10000)
        else:
            valor = 999
        dic_cl = {"nome": cliente[0], "cpf": cliente[1], "salario": cliente[2], "risco": cliente[3], "qant": valor[1],
                  "valor": valor[0]}
        return dic_cl


if __name__ == '__main__':
    pass
