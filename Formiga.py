import numpy as np
import random
import math
import numpy.random as nrand

###############""""""""""""""""""""""###################################
###############""" CLASSE FORMIGA """###################################
###############""""""""""""""""""""""###################################


class Formiga:
    def __init__(self, y, x, grade):
        """
        Inicializa um objeto formiga.
        Esta classe eh apenas uma formiga, sem memoria
        :param y: A localizacao em que foi inicializada
        :param x: A localizacao em que foi inicializada
        :param grade: uma referencia para a grade
        """
        self.local = np.array([y, x])
        self.carregando = grade.get_grade()[y][x]
        self.grade = grade
        self.max_passo = int(50/2)
        self.PP = 0.6
        self.PS = 0.4

    def move(self, n, c):
        """
        Uma funcao recursiva para mover as formigas atraves da grade
        """
        # tamanho de cada passo
        tam_passo = random.randint(1, self.max_passo)
        # Adiciona vetor (-1,+1) * tam_passo na localizacao das formigas
        self.local += nrand.randint(-1 * tam_passo, 1 * tam_passo, 2)
        # Mod na nova localizacao pelo tamanho da grade para prevenir overflow
        self.local = np.mod(self.local, self.grade.dim)
        # Pega o objeto nesta localizacao da grade
        obj = self.grade.get_grade()[self.local[0]][self.local[1]]
        # Se a celula esta ocupada, mova-se novamente
        if obj is not None:
            # Se a formiga nao esta carregando um objeto
            if self.carregando is None:
                # Verifica se a formiga pegou o objeto
                pp = self.prob_pegar(n, c)
                rr = random.random()
                if pp >= rr:  # self.PP:
                    #print "pp", pp, "rr", rr
                    # Pega o objeto e remove da grade
                    self.carregando = obj
                    self.grade.get_grade()[self.local[0]][self.local[1]] = None
                # Se nao pegou, entao mova-se
                else:
                    self.move(n, c)
            # Se estiver carregando um objeto, apenas mova-se
            else:
                self.move(n, c)
        # Se estiver em uma celula vazia
        else:
            if self.carregando is not None:
                # Verifica se a formiga soltou o objeto
                ps = self.prob_soltar(n, c)
                rr2 = random.random()
                if ps >= rr2:  # self.PS:
                    #print "ps", ps, "rr2", rr2
                    # Solte o objeto na celula vazia
                    self.grade.get_grade()[self.local[0]][self.local[1]] = self.carregando
                    self.carregando = None

    def prob_pegar(self, n, c):
        """
        Retorna a probabilidade de pegar um objeto
        :param n: Tamanho da vizinhanca
        :return: probabilidade de pegar
        """
        formiga = self.grade.get_grade()[self.local[0]][self.local[1]]
        #return 1 - self.grade.get_probabilidade(
        #    formiga, self.local[0], self.local[1], n, c)
        f = 1 - self.grade.get_probabilidade(formiga, self.local[0], self.local[1], n, c)
        pp = 1 - math.pow((self.PP / (self.PP + f)), 2)
        #print "PP:", pp , " F:", f
        return f

    def prob_soltar(self, n, c):
        """
        Retorna a probabilidade de soltar um objeto
        :return: probabilidade de soltar
        """
        formiga = self.carregando
        #return self.grade.get_probabilidade(
        #   formiga, self.local[0], self.local[1], n, c)
        f = self.grade.get_probabilidade(formiga, self.local[0], self.local[1], n, c)
        #ps = math.pow((f / (self.PS + f)), 2)
        #print "PS:", ps , " F:", f
        return f