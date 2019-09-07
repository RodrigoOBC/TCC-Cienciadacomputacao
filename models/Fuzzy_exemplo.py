import numpy as np
import skfuzzy as fuzz


def calculos(exercicio, taxa_morte_municipio, cancer_risco, idade, imc, idade_sexo, frequencia_hospitalar):
    x_exercicios = np.arange(0, 300, 1)  # execicios por dia [0,7]
    x_taxa_morte_municipio = np.arange(0, 301, 1)  # taxa de homicidios por ano [0,300]
    x_cancer_risco = np.arange(0, 101, 1)  # historico de cancer 0 para ter cancer, 1 para não ter cancer  [0,300]
    x_saida = np.arange(0, 101, 1)  # saida em porcento

    print(x_saida)

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

    # imc

    # cancer risco

    ''' cancer ficará para a proxima implemntação'''

    cancer_baixo = fuzz.trimf(x_cancer_risco, [0, 30, 34])
    cancer_medio = fuzz.trimf(x_cancer_risco, [32, 50, 60])
    cancer_alto = fuzz.trimf(x_cancer_risco, [58, 70, 100])




    # saida

    perigo_muito_baixo_x = fuzz.trimf(x_saida, [0, 10, 20])
    perigo_baixo_x = fuzz.trimf(x_saida, [15, 30, 40])
    perigo_medio_x = fuzz.trimf(x_saida, [40, 50, 60])
    perigo_alto_x = fuzz.trimf(x_saida, [60, 70, 80])
    perigo_de_risco_x = fuzz.trimf(x_saida, [80, 90, 100])

    # # Definindo os leveis de cada perigo
    # exercicio_level_baixo = fuzz.interp_membership(x_exercicios, exercicio_baixo, exercicio)
    # exercicio_level_normal = fuzz.interp_membership(x_exercicios, exercicio_normal, exercicio)
    # exercicio_level_alto = fuzz.interp_membership(x_exercicios, exercicio_alto, exercicio)
    #
    # # fazendo a vendo qual a relação dos municipios e classificando
    # taxa_morte_municipio_level_muito_baixo_ = fuzz.interp_membership(x_taxa_morte_municipio,
    #                                                                  taxa_morte_municipio_baixissimo,
    #                                                                  taxa_morte_municipio)
    # taxa_morte_municipio_level_baixo = fuzz.interp_membership(x_taxa_morte_municipio, taxa_morte_municipio_baixo,
    #                                                           taxa_morte_municipio)
    # taxa_morte_municipio_level_normal = fuzz.interp_membership(x_taxa_morte_municipio, taxa_morte_municipio_normal,
    #                                                            taxa_morte_municipio)
    # taxa_morte_municipio_level_alto = fuzz.interp_membership(x_taxa_morte_municipio, taxa_morte_municipio_alto,
    #                                                          taxa_morte_municipio)
    # taxa_morte_municipio_level_de_risco = fuzz.interp_membership(x_taxa_morte_municipio,
    #                                                              taxa_morte_municipio_altissimo,
    #                                                              taxa_morte_municipio)
    #
    # # vendo a realação do cancer
    # cancer_historico_level_baixo = fuzz.interp_membership(x_cancer_risco, cancer_baixo, cancer_risco)
    #
    # cancer_historico_level_medio = fuzz.interp_membership(x_cancer_risco, cancer_medio, cancer_risco)
    #
    # cancer_historico_level_alto = fuzz.interp_membership(x_cancer_risco, cancer_medio, cancer_risco)
    #
    # # perigo altissimo
    #
    # '''
    #     perigo_de_risco_x
    #     ou
    #     taxa_morte_municipio_level_de_risco e (cancer_historico_level_Sim e exercicio_level_baixo)
    #     ou
    #     taxa_morte_municipio_level_de_risco e (cancer_historico_level_Sim,exercicio_level_normal)
    # '''
    #
    # perigo_altissimo = np.fmin(
    #     np.fmin(
    #         np.fmax(taxa_morte_municipio_level_de_risco,
    #                 np.fmax(cancer_historico_level_Sim, exercicio_level_baixo)),
    #         np.fmax(taxa_morte_municipio_level_de_risco,
    #                 np.fmax(cancer_historico_level_Sim, exercicio_level_normal))),
    #     perigo_de_risco_x)
    #
    # '''
    #
    #
    # '''


if __name__ == '__main__':
    pass
