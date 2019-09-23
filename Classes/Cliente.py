from datetime import datetime
import requests
import json


# from app.models.Fuzzy_exemplo import calculos


class Cliente:

    def __init__(self, id=None, Nome=None, CEP=None, idade=None, CPF=None, sexo=None, altura=None, peso=None,
                 salarioM=None, dependentes=None, exercicios=None):
        self.id = id
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

    def calcular_imc(self):
        self.imc = self.peso / (self.altura ** 2)
        return round(self.imc, 2)

    def descobri_idade(self):
        valor = datetime.now().year - self.idade
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
        url_api = (f'http://www.viacep.com.br/ws/{cep.replace("-", "")}/json')
        req = requests.get(url_api)
        if req.status_code == 200:
            dados_json = json.loads(req.text)
            return dados_json['localidade']
        else:
            return 'NaN'

    def arrumar_data(self):
        data = self.idade.split('/')
        data[0], data[1], data[2] = data[2], data[1], data[0]
        self.idade = '/'.join(data)


if __name__ == '__main__':
    data = '28/12/1996'.split('/')
    data[0], data[1], data[2] = data[2], data[1], data[0]
    idade = '/'.join(data)
    print(Cliente(idade=idade).descobri_idade())
