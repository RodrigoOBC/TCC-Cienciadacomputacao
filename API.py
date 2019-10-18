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
        ibd(api.cl1.CPF).inserir_banco_classe(api.cl1)
        salario_anos = api.cl1.valor_do_plano()

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
                valor = resultado_form['CPF_BUSCA'].replace('-', '').replace('.', '')
                json_cliente = B_CLIENTE(valor)
                data = json_cliente.get_json()
                print(data['qant'])
                return render_template('buscar_cliente.html', risco=data['risco'],
                                       nome=data['nome'], cpf=data['cpf'], salario=data['salario'], vezes=data['qant'])
            else:
                return render_template('buscar_cliente.html')
        return render_template('buscar_cliente.html', risco=json_risco['risco'],
                               nome=json_risco['nome'], cpf=json_risco['cpf'], salario=json_risco['salario'],
                               vezes=json_risco['qant'])
    else:
        return redirect(url_for('logar'))


@app1.route('/cadastrar_funcionario', methods=['POST'])
def insert_funcionario():
    pass


# serviços da api

@app1.route('/buscar_cliente/CPF=<CPF>', methods=['GET', "POST"])
def B_CLIENTE(CPF):
    if 'user' in session:
        data = json_transformar().passar_cliente_json(CPF)
        response = app1.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        response = app1.response_class(
            response=json.dumps({"erro": "not user", "login": False}),
            status=404,
            mimetype='application/json'
        )
        return response


@app1.route('/incluir_cliente', methods=['POST'])
def insert_usuario():
    try:
        cpf = request.json['cpf']
        nome = request.json['nome']
        cep = request.json['cep']
        idade = request.json['idade']
        sexo = request.json['sexo']
        altura = request.json['altura']
        peso = request.json['peso']
        salario = request.json['salario']
        dep = request.json['dep']
        ex = request.json['ex']
        risco_c = request.json['risco_c']
        risco = request.json['risco']

        print(cpf, nome)
        response = app1.response_class(
            response=json.dumps({"resultado": "incluido", "login": False}),
            status=201,
            mimetype='application/json'
        )
        return response
    except:
        response = app1.response_class(
            response=json.dumps({"erro": "não incluido", "login": False}),
            status=401,
            mimetype='application/json'
        )
        return response


@app1.route('/insert_funcionario', methods=['POST'])
def insert_funcionario():
    try:
        cpf = request.json['cpf']
        nome = request.json['nome']
        senha = request.json['senha']
        permicao = request.json['permicao']
        email = request.json['email']

        lista_valores = [cpf, nome, senha, permicao, email]
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
