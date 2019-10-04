import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix


class Arvore:
    def __init__(self, IMC, MORTE, ID, EX, RESULT):
        self.imc = IMC
        self.morte = MORTE
        self.id_sexo = ID
        self.exercicio = EX
        self.result = RESULT
        self.df_treino = pd.read_csv(r'C:\Users\rodri\PycharmProjects\TCC_Seguros\Data\Treino_tree.csv', sep=';')
        self.dtree = DecisionTreeClassifier()

    def treinar_arvore(self):
        try:
            X = self.df_treino.drop('RESULTADO', axis=1)
            Y = self.df_treino['RESULTADO']
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.50)
            predictions = self.dtree.predict(X_test)
            log = self.dtree.fit(X_train, y_train)
            return predictions
        except:
            return False

    def segmentar_valores(self):
        data = {'IMC': self.imc, 'MORTE': self.morte, 'ID': self.id_sexo, 'EX': self.exercicio}
        x_test = pd.DataFrame(data=data, index=[0])
        predictions = self.dtree.predict(x_test)
        self.colocar_dados_dataframe(x_test)
        if predictions[0] == self.result:
            return self.result
        elif predictions[0] > self.result:
            return predictions[0]
        else:
            return self.result

    def colocar_dados_dataframe(self, x_test):
        self.df_treino.append(data=x_test, ignore_index='False')
