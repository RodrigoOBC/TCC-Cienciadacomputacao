import numpy as np
import skfuzzy as fuzz
from Classes.Cliente import Cliente



def calculos(exercicio, taxa_morte_municipio, cancer_risco, idade, imc, sexo, idade_sexo):
    x_exercicios = np.arange(0, 300, 1)  # execicios por dia [0,7]
    x_taxa_morte_municipio = np.arange(0, 301, 1)  # taxa de homicidios por ano [0,300]
    x_idade = np.arange(0, 19, 1)  # idade de [0,18] considerando o tempo que falta para mudar de turno
    x_saida = np.arange(0, 101, 1)  # saida em porcento
    x_imc = np.arange(0, 51, 1)  # IMC
    x_idade_sexo = np.arange(0, 101, 1)  # resultado de uma função relacionada a idade e sexo
    x_cancer_risco = np.arange(0, 101, 1)  # risco de cancer resultado da função do cancer


    # idade risco

    idade_baixo = fuzz.trimf(x_idade, [0, 3, 6])
    idade_media = fuzz.trimf(x_idade, [5, 8, 12])
    idade_alta = fuzz.trimf(x_idade, [11, 14, 18])

    # exercicio risco

    if 18 <= idade <= 64:
        exercicio_baixo = fuzz.trimf(x_exercicios, [0, 20, 30])
        exercicio_normal = fuzz.trimf(x_exercicios, [28, 50, 60])
        exercicio_alto = fuzz.trimf(x_exercicios, [58, 60, 300])
    elif idade < 18:
        exercicio_baixo = fuzz.trimf(x_exercicios, [0, 50, 75])
        exercicio_normal = fuzz.trimf(x_exercicios, [75, 150, 214])
        exercicio_alto = fuzz.trimf(x_exercicios, [149, 235, 300])

    # municipio risco

    taxa_morte_municipio_baixissimo = fuzz.trimf(x_taxa_morte_municipio, [0, 10, 20])
    taxa_morte_municipio_baixo = fuzz.trimf(x_taxa_morte_municipio, [20, 30, 40])
    taxa_morte_municipio_normal = fuzz.trimf(x_taxa_morte_municipio, [40, 50, 60])
    taxa_morte_municipio_alto = fuzz.trimf(x_taxa_morte_municipio, [60, 70, 80])
    taxa_morte_municipio_altissimo = fuzz.trimf(x_taxa_morte_municipio, [80, 100, 200])

    # IMC
    if sexo == 'M':
        imc_baixo = fuzz.trimf(x_imc, [0, 10, 20])
        imc_medio = fuzz.trimf(x_imc, [19, 20, 24])
        imc_O_leve = fuzz.trimf(x_imc, [23, 26, 29])
        imc_O_moderada = fuzz.trimf(x_imc, [28, 35, 39])
        imc_O_Morbida = fuzz.trimf(x_imc, [38, 45, 50])
    elif sexo == 'F':
        imc_baixo = fuzz.trimf(x_imc, [0, 5, 19])
        imc_medio = fuzz.trimf(x_imc, [19, 20, 24])
        imc_O_leve = fuzz.trimf(x_imc, [23, 26, 29])
        imc_O_moderada = fuzz.trimf(x_imc, [28, 35, 39])
        imc_O_Morbida = fuzz.trimf(x_imc, [38, 45, 50])



    # Diabetes

    cancer_baixo = fuzz.trimf(x_cancer_risco, [0, 10, 30])
    cancer_medio = fuzz.trimf(x_cancer_risco, [28, 40, 50])
    cancer_alto = fuzz.trimf(x_cancer_risco, [48, 60, 70])
    cancer_altissimo = fuzz.trimf(x_cancer_risco, [68, 80, 100])

    # idade sexo

    idade_sexo_baixo = fuzz.trimf(x_idade_sexo, [0, 10, 30])
    idade_sexo_medio = fuzz.trimf(x_idade_sexo, [28, 40, 50])
    idade_sexo_alto = fuzz.trimf(x_idade_sexo, [48, 60, 70])
    idade_sexo_altissimo = fuzz.trimf(x_idade_sexo, [68, 80, 100])

    # saida

    perigo_muito_baixo_x = fuzz.trimf(x_saida, [0, 10, 20])
    perigo_baixo_x = fuzz.trimf(x_saida, [15, 30, 40])
    perigo_medio_x = fuzz.trimf(x_saida, [40, 50, 60])
    perigo_alto_x = fuzz.trimf(x_saida, [60, 70, 80])
    perigo_de_risco_x = fuzz.trimf(x_saida, [80, 90, 100])

    # Definindo os leveis de cada perigo
    exercicio_level_baixo = fuzz.interp_membership(x_exercicios, exercicio_baixo, exercicio)
    exercicio_level_normal = fuzz.interp_membership(x_exercicios, exercicio_normal, exercicio)
    exercicio_level_alto = fuzz.interp_membership(x_exercicios, exercicio_alto, exercicio)

    # fazendo a vendo qual a relação IMC e classificando

    imc_level_baixo = fuzz.interp_membership(x_imc, imc_baixo, imc)
    imc_level_medio = fuzz.interp_membership(x_imc, imc_medio, imc)
    imc_level_alto = fuzz.interp_membership(x_imc, imc_O_leve, imc)
    imc_level_muito_alto = fuzz.interp_membership(x_imc, imc_O_moderada, imc)
    imc_level_negado = fuzz.interp_membership(x_imc, imc_O_Morbida, imc)

    # fazendo a vendo qual a relação dos municipios e classificando

    taxa_morte_municipio_level_muito_baixo_ = fuzz.interp_membership(x_taxa_morte_municipio,
                                                                     taxa_morte_municipio_baixissimo,
                                                                     taxa_morte_municipio)
    taxa_morte_municipio_level_baixo = fuzz.interp_membership(x_taxa_morte_municipio,
                                                              taxa_morte_municipio_baixo,
                                                              taxa_morte_municipio)
    taxa_morte_municipio_level_normal = fuzz.interp_membership(x_taxa_morte_municipio,
                                                               taxa_morte_municipio_normal,
                                                               taxa_morte_municipio)
    taxa_morte_municipio_level_alto = fuzz.interp_membership(x_taxa_morte_municipio, taxa_morte_municipio_alto,
                                                             taxa_morte_municipio)
    taxa_morte_municipio_level_MA = fuzz.interp_membership(x_taxa_morte_municipio,
                                                           taxa_morte_municipio_altissimo,
                                                           taxa_morte_municipio)

    # fazendo a vendo qual a relação idade e classificando

    taxa_idade_level_baixo = fuzz.interp_membership(x_idade, idade_baixo, idade)
    taxa_idade_level_normal = fuzz.interp_membership(x_idade, idade_media, idade)
    taxa_idade_level_alta = fuzz.interp_membership(x_idade, idade_alta, idade)

    # fazendo a vendo qual a relação idade_sexo e classificando

    taxa_IS_baixo = fuzz.interp_membership(x_idade_sexo, idade_sexo_baixo, idade_sexo)
    taxa_IS_medio = fuzz.interp_membership(x_idade_sexo, idade_sexo_medio, idade_sexo)
    taxa_IS_alto = fuzz.interp_membership(x_idade_sexo, idade_sexo_alto, idade_sexo)
    taxa_IS_MA = fuzz.interp_membership(x_idade_sexo, idade_sexo_altissimo, idade_sexo)

    # fazendo a vendo qual a relação cancer e classificando

    taxa_cancer_baixo = fuzz.interp_membership(x_cancer_risco, cancer_baixo, cancer_risco)
    taxa_cancer_medio = fuzz.interp_membership(x_cancer_risco, cancer_medio, cancer_risco)
    taxa_cancer_alto = fuzz.interp_membership(x_cancer_risco, cancer_alto, cancer_risco)
    taxa_cancer_MA = fuzz.interp_membership(x_cancer_risco, cancer_altissimo, cancer_risco)



    ''' 
    aqui será implementada as funções fuzzy para que tenhamos uma logica de 
    1- Risco altissimo
    2 - Risco alto
    3 - Risco medio
    4- Risco baixo
    
    '''

    return 'foi'

if __name__ == '__main__':
    C1 = Cliente(id=1, Nome='Rodrigo', CEP=25515530, idade=23, CPF=123, sexo='F', altura=1.75,
                 peso=75, doenca_cronica=True, salarioM=1200, dependentes=True)
    idade = C1.idade
    sexo = C1.sexo
    imc = C1.calcular_imc()
    idade_S = C1.idade_sexo()

