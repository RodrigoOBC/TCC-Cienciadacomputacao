import json

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
from numpy import random as rd
from flask_json import FlaskJSON, JsonError, json_response, as_json
import os
from Classes.Cliente import Cliente as cl
from Classes.login_sessao import Sessao as se
from Classes.Banco_de_Dados import Conectar as co
from Classes.Banco_de_Dados import Interar_BD_cliente as ibd
from models.Fuzzy_exemplo import Calculos
from models.Arvore_decisao import Arvore
from Classes.Json_sql import json_transformar, buscar_dados


class api:
    def __init__(self):
        self.S1 = se()
        self.cl1 = None
        self.tree = None
        self.predicao = None
        self.dados_municipio = None


api = api()
app1 = Flask(__name__)
app1.secret_key = os.urandom(24)


@app1.route('/login', methods=['GET', "POST"])
@app1.route('/', methods=['GET', "POST"])
def Login():
    if 'user' in session:
        return redirect(url_for('Cadastrar_cliente'))
    if request.method == 'POST':
        rep = True
        resultado_form = request.form.to_dict()
        usuario, passw = resultado_form['CPF_NAME'], resultado_form['login']
        if api.S1.logar(usuario, passw):
            session['user'] = usuario
            api.S1.CPF = usuario
            api.S1.id_sessao = rd.random_integers(1, 100000)
            while (rep == True):
                if api.S1.buscar_sessao():
                    api.S1.id_sessao = rd.random_integers(1, 10000000)
                    rep = True
                else:
                    rep = False
            api.S1.acao = True
            return redirect(url_for('logar'))
        else:
            return render_template("login.html", erro=False)
    return render_template("login.html")


@app1.route('/home', methods=['GET', "POST"])
def Cadastrar_cliente():
    if 'user' in session:
        api.cl1 = None
        if request.method == 'POST':
            resultado_form = request.form.to_dict()
            Nome = resultado_form['Nome_input']
            CEP = resultado_form['CEP_input']
            CPF = resultado_form['CPF_input']
            Idade = resultado_form['Idade_input']
            Sexo = resultado_form['Sexo_input']
            Peso = int(resultado_form['Peso_input'])
            Altura = float(resultado_form['Altura_input'])
            Salario = int(resultado_form['Salario_input'])
            Exercicio = int(resultado_form['Exercicio_input'])

            api.cl1 = cl(Nome=Nome, CEP=CEP, idade=Idade, CPF=CPF, sexo=Sexo, altura=Altura, peso=Peso,
                         salarioM=Salario, dependentes=True, exercicios=Exercicio, risco=None)

            return redirect(url_for('buscar'))
        else:
            return render_template('Cadastrarcliente.html', usuario=api.S1.buscar_stauts(), teste=session['user'])
    return redirect(url_for('Login'))


@app1.route('/logando', methods=['GET', "POST"])
def logar():
    if 'user' in session:
        api.S1.registrar_entrada()
        return redirect(url_for('Cadastrar_cliente'))
    return redirect(url_for('Login'))


@app1.route('/Sair')
def sign_out():
    if 'user' in session:
        session.pop('user')
        api.S1.registrar_saida()
        return redirect(url_for('Login'))
    return redirect(url_for('Login'))


@app1.route('/resultado', methods=['GET', "POST"])
def resultado():
    if 'user' in session:
        ca = Calculos(api.cl1, 1200)
        risco = ca.realizar_calculos()
        imc = api.cl1.imc
        id_sexo = api.cl1.idade_sexo()
        ex = api.cl1.execicios
        api.tree = Arvore(IMC=imc, MORTE=api.cl1.buscar_valor_morte(), ID=id_sexo, EX=ex,
                          RESULT=risco)
        api.predicao = api.tree.treinar_arvore()
        risco_tree = api.tree.segmentar_valores()
        cl.risco = risco_tree
        cliente_json = {
            "cpf": api.cl1.CPF,
            "nome": api.cl1.Nome,
            "cep": api.cl1.CEP,
            "idade": api.cl1.arrumar_data(),
            "sexo": api.cl1.sexo,
            "altura": api.cl1.altura,
            "peso": api.cl1.peso,
            "salario": api.cl1.salarioM,
            "dep": api.cl1.dep,
            "risco_c": 0,
            "ex": api.cl1.execicios,
            "risco": cl.risco
        }

        cliente_json = json.dumps(cliente_json)
        resposta = requests.post("http://127.0.0.1:5000/incluir_cliente", json=cliente_json)
        print(resposta)
        salario_anos = api.cl1.valor_do_plano(api.cl1.salarioM)

        risco_json = {
            'risco': cl.risco,
            'cpf': api.cl1.CPF,
            'nome': api.cl1.Nome,
            'salario': salario_anos[0],
            'qant': salario_anos[1],
            'titulo': 'risco',
        }

        response = app1.response_class(
            response=json.dumps(risco_json),
            status=200,
            mimetype='application/json'
        )
        return response
    erro_json = {
        'erro': 'não logado',
        'status': 404,
        'login': '127.0.0.1:8000'
    }

    response = app1.response_class(
        response=json.dumps(erro_json),
        status=404,
        mimetype='application/json'
    )
    return response


@app1.route('/buscar_cliente', methods=['GET', 'POST'])
def buscar():
    if 'user' in session:
        json_risco = resultado().get_json()
        resultado_form = request.form.to_dict()
        if request.method == 'POST':
            if 'CPF_BUSCA' in resultado_form:
                valor = resultado_form['CPF_BUSCA']
                json_cliente = B_CLIENTE(valor)
                data = json_cliente.get_json()
                print(data['qant'])
                return render_template('buscar_cliente.html', risco=data['risco'],
                                       nome=data['nome'], cpf=data['cpf'], salario=data['valor'], vezes=data['qant'])
            else:
                return render_template('buscar_cliente.html')
        return render_template('buscar_cliente.html', risco=json_risco['risco'],
                               nome=json_risco['nome'], cpf=json_risco['cpf'], salario=json_risco['salario'],
                               vezes=json_risco['qant'])
    else:
        return redirect(url_for('logar'))


@app1.route('/cadastrar_funcionario', methods=['GET', 'POST'])
def cadastrar_funcionario():
    if request.method == 'POST':
        resultado_form = request.form
        resultado = requests.post("http://127.0.0.1:5000/insert_funcionario", json=resultado_form)
        print(resultado)
        return render_template('cadastrar_funcionario.html')
    return render_template('cadastrar_funcionario.html')


# serviços da api

@app1.route('/buscar_cliente/CPF=<CPF>', methods=['GET', "POST"])
def B_CLIENTE(CPF):
    data = json_transformar().passar_cliente_json(CPF)
    response = app1.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@app1.route('/calcular', methods=['GET', "POST"])
def calcular():
    try:
        if request.method == 'POST':
            valor = request.get_json()
            cpf = valor['cpf']
            nome = valor['nome']
            cep = valor['cep']
            idade = valor['idade']
            idade2 = valor['idade2']
            sexo = valor['sexo']
            altura = valor['altura']
            peso = valor['peso']
            salario = valor['salario']
            ex = valor['ex']
            mun = valor['mun']
            id_sex = valor['idsx']
            valor , risco = Calculos('nada','nada').calculos(exercicio=ex,
                                                taxa_morte_municipio=mun,
                                                cancer_risco=0,
                                                idade=idade2, imc=(peso/(altura*altura)),
                                                sexo=sexo,
                                                idade_sexo=id_sex)
            api.tree = Arvore(IMC=(peso/(altura*altura)), MORTE=mun, ID=id_sex, EX=ex,
                              RESULT=risco)
            api.predicao = api.tree.treinar_arvore()
            seg = api.tree.segmentar_valores()
            if buscar_dados().inserir_cliente(
                    [cpf, nome, cep, idade, sexo, altura, peso, salario, False, ex, 0, seg]):
                response = app1.response_class(
                    response=json.dumps({"arvore": seg, "fuzzy": valor, "cpf":cpf}),
                    status=201,
                    mimetype='application/json'
                )
                return response
            else:
                response = app1.response_class(
                    response=json.dumps({"erro": "Não incluiu", "login": False}),
                    status=401,
                    mimetype='application/json'
                )
                return response
    except:

        response = app1.response_class(
            response=json.dumps({"erro": "Quebrou", "login": False}),
            status=500,
            mimetype='application/json'
        )
        return response


@app1.route('/incluir_cliente', methods=['POST'])
def insert_usuario():
    try:
        valor = request.get_json()
        valor = json.loads(valor)
        print(type(valor))
        cpf = valor['cpf']
        nome = valor['nome']
        cep = valor['cep']
        idade = valor['idade']
        sexo = valor['sexo']
        altura = valor['altura']
        peso = valor['peso']
        salario = valor['salario']
        dep = valor['dep']
        ex = valor['ex']
        risco_c = valor['risco_c']
        risco = valor['risco']

        if buscar_dados().inserir_cliente(
                [cpf, nome, cep, idade, sexo, altura, peso, salario, dep, ex, risco_c, risco]):
            response = app1.response_class(
                response=json.dumps({"resultado": "incluido", "login": False}),
                status=201,
                mimetype='application/json'
            )
            return response
        else:
            response = app1.response_class(
                response=json.dumps({"erro": "Não incluiu", "login": False}),
                status=401,
                mimetype='application/json'
            )
            return response
    except:

        response = app1.response_class(
            response=json.dumps({"erro": "Quebrou", "login": False}),
            status=500,
            mimetype='application/json'
        )
        return response


@app1.route('/insert_funcionario', methods=['POST'])
def insert_funcionario():
    try:
        print(request.json)
        cpf = request.json['cpf']
        nome = request.json['nome']
        nome += " " + request.json['lastname_input']
        senha = request.json['senha']
        permicao = request.json['permicao']
        email = request.json['email']

        lista_valores = [cpf, senha, nome, permicao, email]
        if buscar_dados().inseri_funcionario(lista_valores):

            response = app1.response_class(
                response=json.dumps({"resultado": "incluido", "login": "func"}),
                status=201,
                mimetype='application/json'
            )
            return response
        else:
            response = app1.response_class(
                response=json.dumps({"resultado": "não incluido", "tabela": "func"}),
                status=401,
                mimetype='application/json'
            )
            return response

    except:
        response = app1.response_class(
            response=json.dumps({"erro": "erro na api", "login": False}),
            status=500,
            mimetype='application/json'
        )
        return response


if __name__ == '__main__':
    app1.run(debug=True)
