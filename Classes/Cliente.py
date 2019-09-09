from datetime import datetime
import requests
import json


class Cliente:

    def __init__(self, id, Nome, CEP, idade, CPF, sexo, altura, peso, doenca_cronica, salarioM, dependentes):
        self.id = id
        self.Nome = Nome
        self.CEP = CEP
        self.idade = datetime.strptime(idade, '%d/%m/%Y').year
        self.CPF = CPF
        self.sexo = sexo
        self.altura = altura
        self.peso = peso
        self.DC = doenca_cronica
        self.salarioM = salarioM
        self.dep = dependentes
        self.imc = None

    def calcular_imc(self):
        self.imc = self.peso / (self.altura ** 2)
        return self.imc

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

    def buscar_municipio(self):
        url_api = (f'http://www.viacep.com.br/ws/{self.CEP}/json')
        req = requests.get(url_api)
        if req.status_code == 200:
            dados_json = json.loads(req.text)
            return dados_json['localidade']
        else:
            return 'NaN'

    def calcular_cancer(self):
        pass