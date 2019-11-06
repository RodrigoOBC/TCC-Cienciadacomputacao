import numpy as np
import skfuzzy as fuzz
from Classes.Cliente import Cliente
from skfuzzy import control as ctrl


class Calculos:

    def __init__(self, Cliente, despesa):
        self.Cl = Cliente
        self.despesa = despesa

    def calculos(self, exercicio, taxa_morte_municipio, cancer_risco, idade, imc, sexo=None, idade_sexo=None) -> tuple:
        '''
        Função que realiza o calculo de risco com o metodo de fuzzy
        :param exercicio: valor de exercicio feito pelo cliente
        :param taxa_morte_municipio: calculo de mortes a cada 100 mil
        :param cancer_risco: valor do risco de se ter cancer
        :param idade: idade do cliente
        :param imc: imc calculado do cliente
        :param sexo: sexo do cliente
        :param idade_sexo: calculo de risco de morte por sexo
        :return: o valor do risco e o cluster que ele faz parte
        '''
        x_cancer_risco = ctrl.Antecedent(np.arange(0, 121, 1),
                                         'cancer')  # risco de cancer resultado da função do cancer
        x_exercicios = ctrl.Antecedent(np.arange(0, 121, 1), 'exercicio')  # execicios por dia [0,7]
        x_taxa_morte_municipio = ctrl.Antecedent(np.arange(0, 301, 1),
                                                 'morte_mun')  # taxa de homicidios por ano [0,300]
        x_saida = ctrl.Antecedent(np.arange(0, 101, 1), 'saida')  # saida em porcento
        x_imc = ctrl.Antecedent(np.arange(0, 51, 1), 'imc')  # IMC
        x_idade_sexo = ctrl.Antecedent(np.arange(0, 101, 1),
                                       'id_sexo')  # resultado de uma função relacionada a idade e sexo

        # exercicio risco

        if 18 <= idade:
            x_exercicios['baixo'] = fuzz.trimf(x_exercicios.universe, [0, 0, 30])
            x_exercicios['medio'] = fuzz.trimf(x_exercicios.universe, [0, 50, 60])
            x_exercicios['alto'] = fuzz.trimf(x_exercicios.universe, [50, 100, 99999])
        elif idade < 18:
            x_exercicios['baixo'] = fuzz.trimf(x_exercicios.universe, [0, 0, 75])
            x_exercicios['medio'] = fuzz.trimf(x_exercicios.universe, [0, 75, 214])
            x_exercicios['medio'] = fuzz.trimf(x_exercicios.universe, [75, 214, 999999])

            # municipio risco

        x_taxa_morte_municipio['baixissimo'] = fuzz.trimf(x_taxa_morte_municipio.universe, [0, 0, 20])
        x_taxa_morte_municipio['baixo'] = fuzz.trimf(x_taxa_morte_municipio.universe, [0, 20, 40])
        x_taxa_morte_municipio['normal'] = fuzz.trimf(x_taxa_morte_municipio.universe, [20, 40, 60])
        x_taxa_morte_municipio['alto'] = fuzz.trimf(x_taxa_morte_municipio.universe, [40, 70, 80])
        x_taxa_morte_municipio['muito alto'] = fuzz.trimf(x_taxa_morte_municipio.universe, [70, 100, 99999])

        # IMC
        if sexo == 'M':
            x_imc['baixo'] = fuzz.trimf(x_imc.universe, [0, 0, 20])
            x_imc['medio'] = fuzz.trimf(x_imc.universe, [0, 20, 24])
            x_imc['OL'] = fuzz.trimf(x_imc.universe, [20, 24, 29])
            x_imc['OM'] = fuzz.trimf(x_imc.universe, [24, 29, 39])
            x_imc['OMB'] = fuzz.trimf(x_imc.universe, [29, 39, 99999])
        elif sexo == 'F':
            x_imc['baixo'] = fuzz.trimf(x_imc.universe, [0, 0, 19])
            x_imc['medio'] = fuzz.trimf(x_imc.universe, [0, 19, 23])
            x_imc['OL'] = fuzz.trimf(x_imc.universe, [19, 23, 30])
            x_imc['OM'] = fuzz.trimf(x_imc.universe, [23, 30, 35])
            x_imc['OMB'] = fuzz.trimf(x_imc.universe, [30, 35, 99999])

        # Diabetes

        cancer_baixo = fuzz.trimf(x_cancer_risco, [0, 10, 30])
        cancer_medio = fuzz.trimf(x_cancer_risco, [10, 40, 50])
        cancer_alto = fuzz.trimf(x_cancer_risco, [45, 60, 70])
        cancer_altissimo = fuzz.trimf(x_cancer_risco, [65, 80, 100])

        # idade sexo

        x_idade_sexo['baixo'] = fuzz.trimf(x_idade_sexo.universe, [0, 0, 30])
        x_idade_sexo['medio'] = fuzz.trimf(x_idade_sexo.universe, [0, 30, 50])
        x_idade_sexo['Alto'] = fuzz.trimf(x_idade_sexo.universe, [30, 50, 70])
        x_idade_sexo['Altissimo'] = fuzz.trimf(x_idade_sexo.universe, [50, 70, 99999])
        # saida

        x_saida['baixo'] = fuzz.trimf(x_saida.universe, [0, 0, 20])
        x_saida['medio'] = fuzz.trimf(x_saida.universe, [0, 20, 49])
        x_saida['alto'] = fuzz.trimf(x_saida.universe, [20, 49, 80])
        x_saida['negado'] = fuzz.trimf(x_saida.universe, [49, 80, 9999])

        ''' 
        aqui será implementada as funções fuzzy para que tenhamos uma logica de 
        1- Risco altissimo
        2 - Risco alto
        3 - Risco medio
        4- Risco baixo
        
        '''

        regraB1 = ctrl.Rule(x_exercicios['alto'] & x_imc['baixo'] & (
                (x_taxa_morte_municipio['baixissimo'] | x_taxa_morte_municipio['baixo']) & (
                x_idade_sexo['baixo'] | x_idade_sexo['medio'])), x_saida['baixo'])
        regraB2 = ctrl.Rule(x_exercicios['alto'] & x_imc['medio'] & (
                (x_taxa_morte_municipio['baixissimo'] | x_taxa_morte_municipio['baixo']) & (
                x_idade_sexo['baixo'] | x_idade_sexo['medio'])), x_saida['baixo'])

        regraM1 = ctrl.Rule(x_exercicios['alto'] & x_imc['baixo'] &
                            (x_taxa_morte_municipio['baixo'] | x_taxa_morte_municipio['normal'] |
                             x_taxa_morte_municipio['alto']) &
                            (x_idade_sexo['medio'] | x_idade_sexo['Alto']), x_saida['medio']
                            )

        regraM2 = ctrl.Rule(x_exercicios['alto'] & x_imc['medio'] &
                            (x_taxa_morte_municipio['baixo'] | x_taxa_morte_municipio['normal'] |
                             x_taxa_morte_municipio['alto']) &
                            (x_idade_sexo['medio'] | x_idade_sexo['Alto']), x_saida['medio']

                            )

        regraM3 = ctrl.Rule(x_exercicios['alto'] & x_imc['OL'] &
                            (x_taxa_morte_municipio['baixo'] | x_taxa_morte_municipio['normal'] |
                             x_taxa_morte_municipio['alto']) &
                            (x_idade_sexo['medio'] | x_idade_sexo['Alto']), x_saida['medio']
                            )

        regraA1 = ctrl.Rule(x_exercicios['alto'] & x_imc['medio'] &
                            (x_taxa_morte_municipio['normal'] | x_taxa_morte_municipio['alto'] |
                             x_taxa_morte_municipio['muito alto']) & (
                                    x_idade_sexo['medio'] | x_idade_sexo['Alto'] | x_idade_sexo['Altissimo']),
                            x_saida['alto']

                            )

        regraA2 = ctrl.Rule(x_exercicios['alto'] & x_imc['OL'] &
                            (x_taxa_morte_municipio['normal'] | x_taxa_morte_municipio['alto'] |
                             x_taxa_morte_municipio['muito alto']) & (
                                    x_idade_sexo['medio'] | x_idade_sexo['Alto'] | x_idade_sexo['Altissimo']),
                            x_saida['alto'])

        regraA3 = ctrl.Rule(x_exercicios['alto'] & x_imc['OM'] &
                            (x_taxa_morte_municipio['normal'] | x_taxa_morte_municipio['alto'] |
                             x_taxa_morte_municipio['muito alto']) & (
                                    x_idade_sexo['medio'] | x_idade_sexo['Alto'] | x_idade_sexo['Altissimo']),
                            x_saida['alto'])

        regraA4 = ctrl.Rule(x_exercicios['medio'] & x_imc['medio'] &
                            (x_taxa_morte_municipio['normal'] | x_taxa_morte_municipio['alto'] |
                             x_taxa_morte_municipio['muito alto']) & (
                                    x_idade_sexo['medio'] | x_idade_sexo['Alto'] | x_idade_sexo['Altissimo']),
                            x_saida['alto']

                            )

        regraA5 = ctrl.Rule(x_exercicios['medio'] & x_imc['OL'] &
                            (x_taxa_morte_municipio['normal'] | x_taxa_morte_municipio['alto'] |
                             x_taxa_morte_municipio['muito alto']) & (
                                    x_idade_sexo['medio'] | x_idade_sexo['Alto'] | x_idade_sexo['Altissimo']),
                            x_saida['alto'])

        regraA6 = ctrl.Rule(x_exercicios['medio'] & x_imc['OM'] &
                            (x_taxa_morte_municipio['normal'] | x_taxa_morte_municipio['alto'] |
                             x_taxa_morte_municipio['muito alto']) & (
                                    x_idade_sexo['medio'] | x_idade_sexo['Alto'] | x_idade_sexo['Altissimo']),
                            x_saida['alto'])

        regraA7 = ctrl.Rule(x_exercicios['baixo'] & x_imc['medio'] &
                            (x_taxa_morte_municipio['normal'] | x_taxa_morte_municipio['alto'] |
                             x_taxa_morte_municipio['muito alto']) & (
                                    x_idade_sexo['medio'] | x_idade_sexo['Alto'] | x_idade_sexo['Altissimo']),
                            x_saida['alto']

                            )

        regraA8 = ctrl.Rule(x_exercicios['baixo'] & x_imc['OL'] &
                            (x_taxa_morte_municipio['normal'] | x_taxa_morte_municipio['alto'] |
                             x_taxa_morte_municipio['muito alto']) & (
                                    x_idade_sexo['medio'] | x_idade_sexo['Alto'] | x_idade_sexo['Altissimo']),
                            x_saida['alto'])

        regraA9 = ctrl.Rule(x_exercicios['baixo'] & x_imc['OM'] &
                            (x_taxa_morte_municipio['normal'] | x_taxa_morte_municipio['alto'] |
                             x_taxa_morte_municipio['muito alto']) & (
                                    x_idade_sexo['medio'] | x_idade_sexo['Alto'] | x_idade_sexo['Altissimo']),
                            x_saida['alto'])

        regraN1 = ctrl.Rule(x_exercicios['baixo'] & x_imc['OMB'] & (
                x_taxa_morte_municipio['baixissimo'] | x_taxa_morte_municipio['baixo'] | x_taxa_morte_municipio[
            'normal'] | x_taxa_morte_municipio['alto'] |
                x_taxa_morte_municipio['muito alto']) & (
                                    x_idade_sexo['medio'] | x_idade_sexo['Alto'] | x_idade_sexo['Altissimo']),
                            x_saida['alto'])

        '''  perigo ou (((EA ou EM) ou EB) ou ((imcb ou imvm)ou imca)  ou                          '''
        controle_regras = ctrl.ControlSystem(
            [regraB1, regraB2, regraA1, regraA2, regraA3, regraA4, regraA5, regraA6, regraA7, regraA8, regraA9, regraM1,
             regraM2, regraM3, regraN1])
        gerador_risco = ctrl.ControlSystemSimulation(controle_regras)

        return (self.calculo_valores(result), result)

    def calculo_valores(self, porcento) -> str:
        '''
        Função que classifica o em clusters de acordo com a porcentagem de risco apresentada por ele

        :param porcento: Valor da porcentagem de risco atribuida ao cliente
        :return: O grupo de risco pertencente.
        '''
        if porcento <= 10:
            return 'A'
        elif 10 < porcento <= 50:
            return 'B'
        elif 51 <= porcento < 80:
            return 'C'
        elif porcento >= 80:
            return 'D'

    def realizar_calculos(self):
        nivel_risco, taxa_risco = self.calculos(exercicio=self.Cl.execicios,
                                                taxa_morte_municipio=self.Cl.buscar_valor_morte(),
                                                cancer_risco=np.random.random_integers(1, 50),
                                                idade=self.Cl.descobri_idade(), imc=self.Cl.calcular_imc(),
                                                sexo=self.Cl.sexo,
                                                idade_sexo=self.Cl.idade_sexo())
        return nivel_risco


if __name__ == '__main__':
    pass
