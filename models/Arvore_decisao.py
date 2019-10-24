import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sqlalchemy.engine import create_engine


class Arvore:
    def __init__(self, IMC, MORTE, ID, EX, RESULT):
        self.imc = IMC
        self.morte = MORTE
        self.id_sexo = ID
        self.exercicio = EX
        self.result = RESULT
        self.engine = create_engine("postgres://postgres:Meteoro585@localhost:5432/tcc")
        self.df_treino = None
        self.dtree = DecisionTreeClassifier()

    def treinar_arvore(self):
        '''
        Função para treinamento da arvore baseado nos dados contidos no Banco de dados
        :return: True para treinametno correto, False para falha
        '''
        try:
            conn = self.engine.raw_connection()
            self.df_treino = pd.read_sql('select * from dados_arvore limit 300', conn)
            X = self.df_treino.drop('resultado', axis=1)
            Y = self.df_treino['resultado']
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.50)
            log = self.dtree.fit(X_train, y_train)
            return True
        except:
            return False

    def segmentar_valores(self):
        '''
        Função que seguimenta os clientes de acordo com seu risco usando arvore de decisão
        :return: Grupo em que o cliente faz parte
        '''
        data = {'imc': self.imc, 'morte': self.morte, 'id': self.id_sexo, 'ex': self.exercicio}
        x_test = pd.DataFrame(data=data, index=[0])
        predictions = self.dtree.predict(x_test)
        x_test['resultado'] = predictions
        self.colocar_dados_dataframe(x_test)
        if predictions[0] == self.result:
            return self.result
        else:
            return predictions[0]

    def colocar_dados_dataframe(self, x_test):
        self.df_treino.append(x_test, ignore_index='False', sort='False')


if __name__ == '__main__':
    pass
