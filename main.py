#!/usr/bin/env python

""" Programa que simula comportamento de formigas"""
""" Usado para mineiracao de dados """

from Dado import *
from Formiga import *
from Grade import *

import os
from Tkinter import *
from easygui import *
import operator
import sys
import math
import numpy as np
import random
import numpy.random as nrand

__author__ = "Daniel S. Camargo"
__copyright__ = "Copyleft"
__license__ = "GPL v2"
__email__ = "daniel@colmeia.udesc.br"


##############""""""""""""""""""""##############
##############""" CLASSE MAIN  """##############
##############""""""""""""""""""""##############
class Main:

    def __init__(self):
        pass

    def gui(self):
        """
        Metodo que possibilita a entrada de dados personalizados ou padronizados
        GUI = Graphical User Interface
        """
        title = "Escolha uma opcao"
        message = "Deseja personalizar os dados de entrada?"
        default = [50, 50, 25, 50000, 2, 20, 500]
        ret = []
        if boolbox(message, title, ["Sim", "Nao, execute com valores padrao"]):
            title = "Entrada de dados"
            msg = "Entre com os valores desejados"
            fieldNames = ["Altura","Largura","Formigas","Simulacoes","Vizinhanca", "Convergencia","Frequencia"]
            string = multenterbox(msg, title, fieldNames, default)
            for i in range(len(fieldNames)):
                ret.append(int(string[i]))
        else:
            ret = default
        print "Parametros:  ", ret
        self.run(ret)

    def run(self, args):
        """
        Metodo principal que executa os algoritmos
        0:altura, 1:largura, 2:formigas, 3:simulacoes, 4:n, 5:c, 6:freq
        """
        # Inicializa a grade
        grade = Grade(args[0], args[1], pasta="imagens/", rand_test=False)
        # Cria as formigas
        formigas_agentes = []
        cont = 0
        for i in range(args[2]):  # formigas
            formiga = Formiga(random.randint(0, args[0] - 1), random.randint(0, args[1] - 1), grade)
            formigas_agentes.append(formiga)
        # Realiza as simulacoes
        for i in range(args[3]):  # simulacoes
            # Em cada simulacao todas as formigas se movem
            for formiga in formigas_agentes:
                formiga.move(args[4], args[5])  # n, c
            # A imagem eh feita a cada sim/freq
            if i % args[6] == 0:
                cont = cont + 1
                titulo = "Figura " + str(cont) + " de " + str(args[3] / args[6])
                print titulo
                nome = "fig" + str(cont).zfill(6)
                grade.plot_grade(titulo, nome, args)


if __name__ == '__main__':
    os.system('rm -rf imagens/*')  # remove os arquivos anteriores
    m = Main()
    try:
        m.gui()
    except ValueError as e:
        print "ERRO ao executar classe principal: ", e
        sys.exit(e)
    gif = os.system('./makeGIF.sh')
    if gif is 0:
        print "Executando 'Animado.gif' no browser para visualizar o resultado."
    else:
        print "Houve um problema ao criar o GIF. ERR: ", gif

#EOF