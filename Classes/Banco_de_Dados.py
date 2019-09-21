import psycopg2
from postgres import Postgres
from datetime import datetime

class Conectar:
    def __init__(self, host, DB, user, password):
        self.host = host
        self.db = DB
        self.user = user
        self.password = password
        self.con = None

    def Conectar(self) -> bool:
        try:
            self.con = Postgres(f"postgres://{self.user}:{self.password}@{self.host}:5432/{self.db}")
        except:
            return False
        finally:
            return True

    def select(self, query):
        try:
            self.Conectar()
            valores = self.con.all(query)
        except:
            return False
        finally:
            return valores

    def update(self, query) -> bool:
        try:
            self.Conectar()
            self.con.run(query)
        except:
            return False
        finally:
            return True

    def insert(self, query):
        try:
            self.Conectar()
            self.con.run(query)
            return True
        except:
            return False

    def login_buscar(self, usuario, senha):
        try:
            self.Conectar()
            valores = self.con.all(
                f"select  Case When Login_user.cpf = '{usuario}' and Login_user.senha = '{senha}' then 'TRUE' Else 'False' End AS COND From Login_user;")
            return valores
        except:
            return False


class Interar_BD:
    def __init__(self, CPF):
        self.CPF = CPF
        self.id_sessao = None
        self.data_hora = datetime.now()
        self.BD = Conectar(host='localhost', DB='tcc', user='postgres', password='Meteoro585')

    def buscar_Valores(self):
        valor = self.BD.select(f"select * from cliente AS c where c.cpf ={self.CPF} ")
        return valor
if __name__ == '__main__':
    pass