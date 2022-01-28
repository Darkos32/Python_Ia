from math import exp
import random


def tabuleiro(n_tabuleiros, n_rainhas):
    tabuleiros = []
    for i in range(0, n_tabuleiros):
        temp = []
        for j in range(0, n_rainhas):
            temp.append(random.randint(0, n_rainhas-1))
        tabuleiros.append(temp)
    return tabuleiros


def isSolucao(estado):
    if numeroAtaques(estado) == 0:
        return True
    return False


def numeroAtaques(estado):
    count = 0
    tam = len(estado)
    for i in range(0, tam):
        for j in range(i+1, tam):
            if abs(estado[i]-estado[j]) == (j-i) or estado[i] == estado[j]:
                count += 1
    return count


def umVizinho(vizinhanca):
    index = random.randint(0, len(vizinhanca)-1)
    return vizinhanca.pop(index)


def todosVizinhos(estado):
    vizinhos = []
    tam = len(estado)
    for i in range(0, 2*tam):
        if i <= tam - 1:
            for j in range(1, 4):
                if estado[i % tam] + j <= 3:
                    vizinho = prox_vizinho_rainha(estado, j, i % tam)
                    vizinhos.append(vizinho)
                else:
                    continue
        else:
            for j in range(1, 4):
                if estado[i % tam] - j >= 0:
                    vizinho = prox_vizinho_rainha(estado, -j, i % tam)
                    vizinhos.append(vizinho)

    return vizinhos


def prox_vizinho_rainha(estado, passo, index):
    prox = list(estado)
    prox[index] += passo
    return prox


def arrayToString(array):
    string = "["
    for s in range(0, len(array)):
        string += "{},".format(array[s]) if s != len(array) - \
            1 else "{}".format(array[s])
    string += "]"
    return string


def nextTemp(alfa, tempAtual):
    return tempAtual*alfa


def simulated_annealing(tempInicial, maxIt, alfa, estadoInicial):
    atual = list(estadoInicial)
    melhor = atual
    tempAtual = tempInicial
    vizinhos = todosVizinhos(atual)
    valorAtual = numeroAtaques(atual)
    valorMelhor = valorAtual
    numeroMelhoras = 0
    numeroTrocasAleatorias = 0
    interacoes = 0
    for i in range(0, maxIt):
        interacoes = i
        vizinho = umVizinho(vizinhos)
        valorVizinho = numeroAtaques(vizinho)
        delta = valorVizinho - valorAtual
        if delta < 0:
            atual = vizinho
            vizinhos = todosVizinhos(atual)
            valorAtual = valorVizinho
            if valorVizinho < valorMelhor:
                melhor = atual
                valorMelhor = valorAtual
                numeroMelhoras += 1
        elif exp(-delta/tempAtual) < random.uniform(0, 1):
            atual = vizinho
            vizinhos = todosVizinhos(atual)
            valorAtual = valorVizinho
            numeroTrocasAleatorias += 1
        tempAtual = alfa*tempAtual
        if vizinhos == []:
            break
    return (melhor, numeroMelhoras, numeroTrocasAleatorias, interacoes)


def runSimulatedAnnealing(nRainhas, temp, maxIt, alfa):
    x = tabuleiro(1, nRainhas)[0]
    resultado = simulated_annealing(temp, maxIt, alfa, x)
    if isSolucao(resultado[0]):
        print(arrayToString(
            resultado[0])+" é solução encontrada após {}".format(resultado[3]) + " interações")
    else:
        print(arrayToString(resultado[0])+" não é solução")


def runFunc(nVezes, *args):
    params = list(args)
    f = params.pop(0)
    for i in range(0, nVezes):
        f(*params)


runFunc(10, runSimulatedAnnealing, 4, 100, 50, 0.9)
