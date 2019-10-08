from datetime import datetime
import requests
import json
from .Banco_de_Dados import Conectar


# from app.models.Fuzzy_exemplo import calculos


class Cliente:

    def __init__(self, Nome=None, CEP=None, idade=None, CPF=None, sexo=None, altura=None, peso=None,
                 salarioM=None, dependentes=None, exercicios=None, risco=None):
        self.id = 0
        self.Nome = Nome
        self.CEP = CEP
        self.idade = idade
        self.CPF = CPF
        self.sexo = sexo
        self.altura = altura
        self.peso = peso
        self.salarioM = salarioM
        self.dep = dependentes
        self.imc = None
        self.execicios = exercicios
        self.risco = risco

    def calcular_imc(self):
        self.imc = self.peso / (self.altura ** 2)
        return round(self.imc, 2)

    def descobri_idade(self):
        ano_certo = self.arrumar_data()
        data = datetime.strptime(ano_certo, '%Y/%m/%d')
        valor = datetime.now().year - data.year
        return valor

    def idade_sexo(self):
        idade = self.descobri_idade()
        if self.sexo == 'M':
            if 0 <= idade <= 15:
                return 32.83
            elif 16 <= idade <= 40:
                return 53.35
            elif 41 <= idade <= 59:
                return 73.53
            else:
                return 87.48
        if self.sexo == 'F':
            if 0 <= idade <= 15:
                return 25.56
            elif 16 <= idade <= 40:
                return 46.22
            elif 41 <= idade <= 59:
                return 70.43
            else:
                return 85.02

    def calcular_exercicios(self):
        result = (self.execicios * 300) / 7
        return result

    def buscar_municipio(self):
        cep = self.CEP
        cep = cep.replace('.', '')
        url_api = f'http://www.viacep.com.br/ws/{cep.replace("-", "")}/json'
        req = requests.get(url_api)
        if req.status_code == 200:
            dados_json = json.loads(req.text)
            return int(str(dados_json['ibge'])[3:])
        else:
            return 'NaN'

    def arrumar_data(self):
        data = self.idade.split('/')
        data[0], data[1], data[2] = data[2], data[1], data[0]
        return '/'.join(data)

    def buscar_valor_morte(self):
        cod_municipio = self.buscar_municipio()
        BD = Conectar(host='localhost', DB='tcc', user='postgres', password='Meteoro585')
        lista_com_val = BD.select(f'select MD.MORTE from Municipio_dados as MD WHERE MD.cod = {cod_municipio};')
        if lista_com_val:
            return lista_com_val[0]
        else:
            return 'fudeu'


if __name__ == '__main__':
    pass
