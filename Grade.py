
import matplotlib.pylab as plt
import numpy as np
import random
import math
import numpy.random as nrand
from Dado import *

##############""""""""""""""""""""###################################
##############""" CLASSE GRADE """###################################
##############""""""""""""""""""""###################################


class Grade:
    def __init__(self, altura, largura, pasta, rand_test=True):
        """
        Este metodo inicializa um objeto grade.
        Uma grade eh basicamente um vetor 2D de objetos Dado.
        :param altura: altura da grade
        :param largura: largura da grade
        :param pasta: pasta onde serao armazenadas as imagens
        """
        self.fileName = "Square1_DataSet_400itens.txt"
        self.pasta = pasta
        # Armazena dimensoes da grade
        self.dim = np.array([altura, largura])
        # Inicializa uma matriz np vazia do tipo objeto Dado
        self.grade = np.empty((altura, largura), dtype=object)
        if rand_test:
            # Usado para preencher a grade randomicamente
            self.grade_rand(0.25)
        else:
            self.grade_arquivo()
        # Faz o redesenho da grade
        plt.ion()
        plt.figure(figsize=(10, 10))
        self.max_d = 0.001

    def grade_arquivo(self):
        """
        Metodo que fornece dados apartir de entrada de arquivo
        """
        with open(self.fileName) as f:
            for cadaLinha in f:
                linha = map(float, cadaLinha.split())
                linhaFloat = [linha[0], linha[1]]
                while True:
                    x = random.randint(0, self.dim[1] - 1)
                    y = random.randint(0, self.dim[0] - 1)
                    if self.grade[y][x] == None:
                        self.grade[y][x] = Dado(linhaFloat)
                        break

    def grade_rand(self, sparse):
        """
        Metodo para inicializar a grade randomicamente
        :sparse: limiar para aceitacao do retorno do random()
        """
        total = 0
        for y in range(self.dim[0]):
            for x in range(self.dim[1]):
                if random.random() <= sparse:
                	# Dicionario com as faixas padrao de 1 a 4
                    dic = {1:[-1, -1], 2:[1, 1], 3:[-1, 1], 4:[1, -1]}
                    r = random.randint(1, 4)
                    d = [nrand.normal(dic[r][0] * 20, 0.25), nrand.normal(dic[r][1] * 20, 0.25)]
                    self.grade[y][x] = Dado(d)  # nrand.normal(-20, 0.25, 2))
                    total += 1
        print "Total de corpos criados: ", total

    def matriz_grade(self):
        """
        Metodo que condensa a grade (Vetor 2D de objetos Dado)
        para uma matriz que pode ser visualizada
        :return: matriz da grade
        """
        matriz = np.empty((self.dim[0], self.dim[1]), dtype=float)
        matriz.fill(0)
        for y in range(self.dim[0]):
            for x in range(self.dim[1]):
                if self.grade[y][x] is not None:
                    matriz[y][x] = self.get_grade()[y][x].abstraia()
        return matriz

    def plot_grade(self, titulo, nome, args, save_figure=True):
        """
        Metodo que plota a representacao 2D da grade
        :param titulo: Contador das imagens
        :param nome: Nome da imagem a ser salva
        :param args: Argumentos usados para executar o teste
        """
        #Opcoes de cor: "RdBu" "seismic" , "RdYlGn", "jet"
        # mais em: http://matplotlib.org/users/colormaps.html
        plt.matshow(self.matriz_grade(), cmap="RdBu", fignum=0)
        # Opcao para salvar imagens
        if save_figure:
            plt.savefig(self.pasta + nome + '.png')
        plt.title(titulo)
        plt.xlabel("Argumentos: " + str(args))
        plt.draw()

    def get_grade(self):
        return self.grade

    def get_probabilidade(self, d, y, x, n, c):
        """
        Pega a probabilidade de largar ou pegar um corpo d
        :param d: o datum
        :param x: a localizacao 'x' do datum / formiga carregando um datum
        :param y: a localizacao y do datum / formiga carregando um datum
        :param n: Tamanho da funcao de vizinhanca
        :param c: constante para controle de convergencia
        :return: probabilidade de algo
        """
        # Inicia a localizacao do x e do y
        y_s = y - n
        x_s = x - n
        total = 0.0
        # Para cada vizinho
        for i in range((n * 2) + 1):
            xi = (x_s + i) % self.dim[0]
            for j in range((n * 2) + 1):
                # Se estivermosprint "probabilidade:", probabilidade olhando para um vizinho
                if j != x and i != y:
                    yj = (y_s + j) % self.dim[1]
                    # Pegue o vizinho 'o'
                    o = self.grade[xi][yj]
                    # Somatorio da distancia de 'o' com 'x'
                    if o is not None:
                        sim = d.distancia(o)
                        total += sim
        #if total < 78.6 and total > 0: asd
        #	return 0.0001
        #cells = math.pow((n * 2) + 1, 2) - 1
        #f = (total) / (20 * cells)
        #probabilidade = max(min(f, 1), 0)
        #print "Total: ", total, " Probabilidade", probabilidade
        #return probabilidade


        # Normaliza a densidade para a maxima distancia vista ate o momento
         md = total / (math.pow((n * 2) + 1, 2) - 1)
         if md > self.max_d:
             self.max_d = md
         densidade = total / (self.max_d * (math.pow((n * 2) + 1, 2) - 1))
         densidade = max(min(densidade, 1), 0) # retorna 0 < d < 1. Se densidade < 0, retorna 0; se > 1 retorna 1
         t = math.exp(-c * densidade)
         probabilidade = (1 - t) / (1 + t)
         return probabilidade