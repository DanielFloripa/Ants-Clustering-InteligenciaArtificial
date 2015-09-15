
import numpy as np
from scipy.spatial import distance


################""""""""""""""""""""###################################
################""" CLASSE DADO  """###################################
################""""""""""""""""""""###################################


class Dado:

    def __init__(self, data):
        """
        Um objeto Dado eh basicamente um vetor nD
        :param data: vetor nD
        """
        self.data = data

    def getDado(self):
        return self.data

    def distancia(self, outroDado):
        """
        Retorna a distancia entre este dado e algum outro dado
        :param outroDado: O outro dado
        :return: distancia (sum squared)
        """
        d = distance.euclidean(self.data, outroDado.data)
        # print "Distancia:", d
        return d
        #diferenca = np.abs(map(operator.sub, self.data, outroDado.data))
        #return np.sum(diferenca ** 2)

    def abstraia(self):
        """
        Metodo para condensar vetor 2D em apenas 1 dado para visualizacao
        Deve ser chamado apenas para criar a matriz e imprimir as cores
        Diferencia os quatro tipos de dados [+,-]:4 / [-,+]:3 / [+,+]:2 / [-,-]:1
        :return: representacao 1D do vetor
        """
        if self.data[0] > 0 and self.data[1] < 0:
            return 4
        if self.data[0] < 0 and self.data[1] > 0:
            return 3
        if self.data[0] > 0 and self.data[1] > 0:
            return 2
        if self.data[0] < 0 and self.data[1] < 0:
            return 1
        else: return 0
        #((self.data[0]) + (self.data[0]))/2 
        #mean = np.mean(self.data)
        #return mean
