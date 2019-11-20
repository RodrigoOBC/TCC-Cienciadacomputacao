import random
from requests import get, post
from bs4 import BeautifulSoup
import pandas as pd
import json

from Classes import Conectar


def generate_cpf():
    cpf = [random.randint(0, 9) for x in range(9)]

    for _ in range(2):
        val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11

        cpf.append(11 - val if val > 1 else 0)

    return '%s%s%s.%s%s%s.%s%s%s-%s%s' % tuple(cpf)

def gerar_cep():
    data = {'acao': 'gerar_cep', 'cep_estado': 'RJ', 'cep_cidade': '', 'somente_numeros': 'N'}
    r = post('https://www.4devs.com.br/ferramentas_online.php', data)
    html = BeautifulSoup(r.text, "html.parser")
    cep = html.find(id="cep").get('value')
    return cep

def gerar_nome(sexo):
    if sexo == "M":
        sexo = "H"
    else:
        sexo = "M"

    data = {'acao': 'gerar_pessoa', 'sexo': sexo}
    r = post('https://www.4devs.com.br/ferramentas_online.php', data)
    html = BeautifulSoup(r.text, "html.parser")
    return r.json()['nome']

def idade_sexo(idade,sexo):
    if sexo == 'M':
        if 0 <= idade <= 15:
            return 32.83
        elif 16 <= idade <= 40:
            return 53.35
        elif 41 <= idade <= 59:
            return 73.53
        else:
            return 87.48
    if sexo == 'F':
        if 0 <= idade <= 15:
            return 25.56
        elif 16 <= idade <= 40:
            return 46.22
        elif 41 <= idade <= 59:
            return 70.43
        else:
            return 85.02

def buscar_municipio(cep):
    cep = cep.replace('.', '')
    url_api = f'http://www.viacep.com.br/ws/{cep.replace("-", "")}/json'
    req = get(url_api)
    if req.status_code == 200:
        dados_json = json.loads(req.text)
        return buscar_morte(int(str(dados_json['ibge'])[3:]))
    else:
        return 'NaN'

def buscar_morte(cod):
    BD = Conectar(host='localhost', DB='tcc', user='postgres', password='Meteoro585')
    lista_com_val = BD.select(f'select MD.MORTE from Municipio_dados as MD WHERE MD.cod = {cod};')
    if lista_com_val:
        return lista_com_val[0]
    else:
        return 'erro'



if __name__ == '__main__':
    df = pd.read_csv('Data/dados_para_analise.csv')
    df = df[df.index > 392]
    for (ALTU, idade, PESO, S) in zip(df['ALTURA'], df['IDADE'], df['PESOS'], df['SEXO']):
        cep = gerar_cep()
        ano = 2019 - idade
        json_cliente = {
            "cpf": generate_cpf(),
            "nome": gerar_nome(S),
            "cep": cep,
            "idade": f"{ano}-12-25",
            "idade2":idade,
            "sexo": S,
            "altura": ALTU,
            "peso": PESO,
            "salario": random.randint(998, 10999),
            "dep": 0,
            "risco_c": 0,
            "ex": random.randint(58, 300),
            "risco": "B",
            "mun": buscar_municipio(cep),
            "idsx": idade_sexo(idade,S)

        }


        r = post('http://127.0.0.1:5000/calcular',json=json_cliente)

        print(r.json())