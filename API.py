from flask import Flask, render_template, request, redirect, url_for, session
from numpy import random as rd
import os
from Classes.Cliente import Cliente as cl
from Classes.login_sessao import Sessao as se
from Classes.Banco_de_Dados import Conectar as co

app1 = Flask(__name__)
app1.secret_key = os.urandom(24)
global S1
global cliente1
S1 = se()


@app1.route('/login', methods=['GET', "POST"])
@app1.route('/', methods=['GET', "POST"])
def Login():
    if request.method == 'POST':
        rep = True
        resultado_form = request.form.to_dict()
        usuario, passw = resultado_form['CPF_NAME'], resultado_form['login']
        if S1.logar(usuario, passw):
            session['user'] = usuario
            S1.CPF = usuario
            S1.id_sessao = rd.random_integers(1, 100000)
            while (rep == True):
                if S1.buscar_sessao():
                    S1.id_sessao = rd.random_integers(1, 10000000)
                    rep = True
                else:
                    rep = False
            S1.acao = True
            return redirect(url_for('logar'))
        else:
            return render_template("login.html", erro=False)
    return render_template("login.html")


@app1.route('/home', methods=['GET', "POST"])
def Home():
    resultado = None
    media = None
    Nome = None
    CEP = None
    erro_home = 'ola'
    if 'user' in session:
        if request.method == 'POST':
            resultado_form = request.form.to_dict()
            cliente1 = cl(Nome=resultado_form['Nome_input'], CEP=resultado_form['CEP_input'], idade='28/12/1996')
            if (cliente1.Nome != '' and cliente1.CEP != '') and (
                    cliente1.Nome is not None and cliente1.CEP is not None):
                return redirect(url_for('logar'))
            else:
                erro_home = 'Todos os Campos são obrigatorios'
                return render_template('Home.html', erro=erro_home)
        else:
            return render_template('Home.html', usuario=session['user'])
    return redirect(url_for('Login'))


@app1.route('/logando', methods=['GET', "POST"])
def logar():
    if 'user' in session:
        S1.registrar_entrada()
        return redirect(url_for('Home'))


@app1.route('/Sair')
def sign_out():
    if 'user' in session:
        session.pop('user')
        S1.registrar_saida()
        return redirect(url_for('Login'))


if __name__ == '__main__':
    app1.run(debug=True)
