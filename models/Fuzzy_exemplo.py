import numpy as np
import skfuzzy as fuzz


def entrada():
    exercicio = 2
    taxa_morte_municipio = 199
    cancer_historico = 1
    exercicio = int((exercicio * 300) / 7)


def calculos(exercicio, taxa_morte_municipio, cancer_historico):
    x_exercicios = np.arange(0, 301, 1)  # execicios por dia [0,7]
    x_taxa_morte_municipio = np.arange(0, 301, 1)  # taxa de homicidios por ano [0,300]
    x_cancer_historico = np.arange(0, 2, 1)  # historico de cancer 0 para ter cancer, 1 para não ter cancer  [0,300]
    x_saida = np.arange(0, 101, 1)  # saida em porcento

    print(x_saida)

    exercicio_baixo = fuzz.trimf(x_exercicios, [0, 64, 128])
    exercicio_normal = fuzz.trimf(x_exercicios, [85, 150, 214])
    exercicio_alto = fuzz.trimf(x_exercicios, [171, 235, 300])

    # municipio risco

    taxa_morte_municipio_baixissimo = fuzz.trimf(x_taxa_morte_municipio, [0, 10, 20])
    taxa_morte_municipio_baixo = fuzz.trimf(x_taxa_morte_municipio, [20, 30, 40])
    taxa_morte_municipio_normal = fuzz.trimf(x_taxa_morte_municipio, [40, 50, 60])
    taxa_morte_municipio_alto = fuzz.trimf(x_taxa_morte_municipio, [60, 70, 80])
    taxa_morte_municipio_altissimo = fuzz.trimf(x_taxa_morte_municipio, [80, 100, 200])

    # cancer risco

    cancer_baixo = fuzz.trimf(x_cancer_historico, [0, 0, 1])
    cancer_alto = fuzz.trimf(x_cancer_historico, [1, 1, 1])

    # saida

    perigo_baixissimo_x = fuzz.trimf(x_saida, [0, 10, 20])
    perigo_baixo_x = fuzz.trimf(x_saida, [15, 30, 40])
    perigo_medio_x = fuzz.trimf(x_saida, [40, 50, 60])
    perigo_alto_x = fuzz.trimf(x_saida, [60, 70, 80])
    perigo_muito_alto_x = fuzz.trimf(x_saida, [80, 90, 100])

    exercicio_level_baixo = fuzz.interp_membership(x_exercicios, exercicio_baixo, exercicio)
    exercicio_level_normal = fuzz.interp_membership(x_exercicios, exercicio_normal, exercicio)
    exercicio_level_alto = fuzz.interp_membership(x_exercicios, exercicio_alto, exercicio)

    # fazendo a vendo qual a relação dos municipios e classificando
    taxa_morte_municipio_level_baixissimo = fuzz.interp_membership(x_taxa_morte_municipio,
                                                                   taxa_morte_municipio_baixissimo,
                                                                   taxa_morte_municipio)
    taxa_morte_municipio_level_baixo = fuzz.interp_membership(x_taxa_morte_municipio, taxa_morte_municipio_baixo,
                                                              taxa_morte_municipio)
    taxa_morte_municipio_level_normal = fuzz.interp_membership(x_taxa_morte_municipio, taxa_morte_municipio_normal,
                                                               taxa_morte_municipio)
    taxa_morte_municipio_level_alto = fuzz.interp_membership(x_taxa_morte_municipio, taxa_morte_municipio_alto,
                                                             taxa_morte_municipio)
    taxa_morte_municipio_level_altissimo = fuzz.interp_membership(x_taxa_morte_municipio,
                                                                  taxa_morte_municipio_altissimo,
                                                                  taxa_morte_municipio)

    # vendo a realação do cancer
    cancer_historico_level_Nao = fuzz.interp_membership(x_cancer_historico, cancer_baixo, cancer_historico)
    cancer_historico_level_Sim = fuzz.interp_membership(x_cancer_historico, cancer_alto, cancer_historico)

    # perigo altissimo

    '''
        perigo_muito_alto_x 
        ou 
        taxa_morte_municipio_level_altissimo e (cancer_historico_level_Sim e exercicio_level_baixo)
        ou
        taxa_morte_municipio_level_altissimo e (cancer_historico_level_Sim,exercicio_level_normal)
    '''

    perigo_altissimo = np.fmin(
                        np.fmin(
                                np.fmax(taxa_morte_municipio_level_altissimo,
                                        np.fmax(cancer_historico_level_Sim,exercicio_level_baixo)),
                                        np.fmax(taxa_morte_municipio_level_altissimo,
                                                np.fmax(cancer_historico_level_Sim,exercicio_level_normal))),
                                perigo_muito_alto_x)

    '''
    
    
    '''
