from numpy import random as rd
from datetime import datetime
from Classes.Banco_de_Dados import Conectar as co


class Sessao:
    def __init__(self):
        self.CPF = None
        self.id_sessao = None
        self.data_hora = datetime.now()
        self.BD = co(host='localhost', DB='tcc', user='postgres', password='Meteoro585')
        self.acao = False

    def logoff(self):
        id, self.id_sessao = self.id_sessao, None
        self.registrar_saida(datetime.now())

    def registrar_entrada(self):
        self.BD.insert(query=f"insert into Sessao values ('{self.id_sessao}','{self.CPF}','{str(self.data_hora)}','E')")

    def registrar_saida(self):
        data = datetime.now()
        self.BD.insert(query=f"insert into Sessao values ('{self.id_sessao}','{self.CPF}','{data}','S')")

    def logar(self, usuario, senha):
        Entrada = self.BD.login_buscar(usuario=usuario, senha=senha)
        if Entrada[0] == 'TRUE':
            return True
        else:
            return False

    def buscar_sessao(self):
        valor = self.BD.select(
            query=f"select  Case When sessao.id_sessao = ({self.id_sessao})  then 'TRUE' Else 'False' End AS COND From sessao;")
        if valor[0] == 'TRUE':
            return True
        else:
            return False


if __name__ == '__main__':
    pass
