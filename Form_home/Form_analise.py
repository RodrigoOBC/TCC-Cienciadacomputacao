from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, SelectFieldBase, SubmitField
from wtforms.validators import DataRequired


class Analise_form(FlaskForm):
    Nome = StringField('Nome', validators=[DataRequired()])
    CEP = StringField('CEP', validators=[DataRequired()])
    CPF = StringField('CPF', validators=[DataRequired()])
    idade = StringField('idade', validators=[DataRequired()])
    Sexo = StringField('sexo', validators=[DataRequired()])
    altura = StringField('altura', validators=[DataRequired()])
    peso = StringField('peso', validators=[DataRequired()])
    SalarioMensal = StringField('Salario_mensal', validators=[DataRequired()])
    dep = StringField('dependentes', validators=[DataRequired()])
