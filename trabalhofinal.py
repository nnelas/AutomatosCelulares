#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############
## TRABALHO IA - AUTOMATOS CELULARES
##
## Jorge Loureiro, 21501465
## Nuno Nelas, 21502312
##
##############

import os
import sys
import random

def generateInitRule():

	#inicia uma lista vazia de rules
	listRules = []
	
	#ciclo for de 0 a 79
	#em caso real seria de 0 a 300
	for i in range(0, 1):
	
		#boas rules
		#stor: 339841014795010104073313096675879420072
		#minha1: 315305439436733206442928922878350886964
		#minha2: 67214365413577693017490885819434821140
		#random: random.randint(0,2**128)

		#por cada ciclo vai:
		#gerar novo número decimal de 0 a 2 elevado a 128
		ruleDec = 336232015478787792617042280871785147552
		
		#atribuir o tamanho da regra de 128
		ruleSize = 128
		
		#converter o número decimal aleatório para binário 
		ruleBin = "{0:b}".format(ruleDec)
		
		#fazer padding dessa rule até chegar ao tamanho ruleSize
		padRule = ruleBin.zfill(ruleSize)
		
		#inverter a rule
		revRule = padRule[::-1]
		
		#passar o número binário para uma lista
		rule = [int(i) for i in str(revRule)]
		
		#guardar a nova rule na lista de rules
		listRules.append(rule)

	return listRules


def generateLattice():

	#inicia uma lista de lattices vazia
	listLattices = []
	
	#inicia o contador para o ciclo while
	i = 0

	#ciclo while para gerar 200 lattices, 0 a 199
	#em caso real, seria de 0 a 10000
	while i < 1:
	
		#inicializa as var numZero e numOne para gerar populações com maioria igual de 0 e 1
		numZero = 0
		numOne = 0
		
		#inicia uma lista lattice vazia
		lattice = []
		
		#ciclo for para gerar 101 zeros ou uns
		#em caso real seria range 0 a 301
		for j in range (0,301): 
			#para cada posicao da lista vai gerar um numero aleatorio inteiro de 0 a 1
			#e guardar na lista lattice
			lattice.append(random.randint(0,1))
			
		#para cada elemento da lista lattice
		#vai contar numZero e numOne
		for k in lattice:
			if (k == 0):
				numZero += 1
			elif(k == 1):
				numOne += 1

		#depois, vai chamar a função checkMajority para ver a maioria
		majority = checkMajority(numZero, numOne)
		
		#para verificar se:
		#primeiras 100 lattices têm maioria 0
		#segundas 100 lattices têm maioria 1
		if (i < 3):
			#caso a maioria seja 0,
			#então incrementa o contador i e adiciona a lattice na lista de lattices
			#caso a maioria seja 1
			#não incrementa o contador, ou seja, volta a gerar nova lattice
			if (majority == 0):
				print "lattice accepted"
				print lattice
				i += 1
				listLattices.append(lattice)
		elif (i >= 5):
			if (majority == 0):
				print "lattice denial"
			#caso a maioria seja 1,
			#então incrementa o contador i e adiciona a lattice na lista de lattices
			#caso a maioria seja 0
			#não incrementa o contador, ou seja, volta a gerar nova lattice
			if (majority == 1):
				print lattice
				print "lattice accepted"
				i += 1
				listLattices.append(lattice)

	return listLattices

def ruleOnLattice(listRules, listLattices):
	updatedLattices = []
	
	#por cada rule:
	for i, rule in enumerate (listRules):
	
		#cria lista de scores
		scores = []
		
		#converte rule de binário para decimal para apresentar
		#ao utilizador na linha de comandos
		ruleDec = ''.join(str(x) for x in rule)
		ruleDec = ruleDec[::-1]
		ruleDec = int(ruleDec, 2)
		print "rule in progress: %s" % ruleDec
		
		#por cada lattice:
		for j, lattice in enumerate (listLattices):
		
			#adiciona lattice a processar à lista updatedLattices para depois imprimir
			updatedLattices.append(lattice)
			
			#executa a funcao updateL para correr a rule na lattice
			#guarda o score dessa rule na lista scores
			scores = updateL(lattice, rule, updatedLattices, scores)
			
		#executa a funcao doFitnessForRule e guarda o score da rule	
		scoreOfRule = doFitnessForRule(scores)
		
		#imprime o score da rule
		print "score of rule: %s" % scoreOfRule
		
		#remove a rule para inserir a rule com o score ao lado
		listRules.pop(i)
		listRules.insert(i, [[scoreOfRule], rule])
		
	#depois de correr a lista de rules, chama a funcao getTopRules	
	#getTopRules(listRules)
	return updatedLattices

def updateL (lattice, rule, updatedLattices, scores):

	#Run the automaton for 2L time steps, this should give you a matrix M with dimensions L x 2L
	for j in range(0,202):
		latticeOut = []
		for i in range(len(lattice)):
			ESQESQESQ = (i-3)
			ESQESQ = (i-2)
			ESQ = (i-1)
			DIR = (i+1)
			DIRDIR = (i+2)
			DIRDIRDIR = (i+3)
			if i == (len(lattice) - 1):
				DIR = 0
				DIRDIR = 1
				DIRDIRDIR = 2
				joinNeighboors = ''.join([str(lattice[ESQESQESQ]), str(lattice[ESQESQ]), str(lattice[ESQ]), str(lattice[i]), str(lattice[DIR]), str(lattice[DIRDIR]), str(lattice[DIRDIRDIR])])
				check = int(joinNeighboors, 2)
				latticeOut.append(rule[check])
			elif i == (len(lattice) - 2):
				DIRDIR = 0
				DIRDIRDIR = 1
				joinNeighboors = ''.join([str(lattice[ESQESQESQ]), str(lattice[ESQESQ]), str(lattice[ESQ]), str(lattice[i]), str(lattice[DIR]), str(lattice[DIRDIR]), str(lattice[DIRDIRDIR])])
				check = int(joinNeighboors, 2)
				latticeOut.append(rule[check])
			elif i == (len(lattice) - 3):
				DIRDIRDIR = 0
				joinNeighboors = ''.join([str(lattice[ESQESQESQ]), str(lattice[ESQESQ]), str(lattice[ESQ]), str(lattice[i]), str(lattice[DIR]), str(lattice[DIRDIR]), str(lattice[DIRDIRDIR])])
				check = int(joinNeighboors, 2)
				latticeOut.append(rule[check])
			elif i == 0:
				ESQESQ = (len(lattice) - 2)
				ESQESQESQ = (len(lattice) - 3)
				joinNeighboors = ''.join([str(lattice[ESQESQESQ]), str(lattice[ESQESQ]), str(lattice[ESQ]), str(lattice[i]), str(lattice[DIR]), str(lattice[DIRDIR]), str(lattice[DIRDIRDIR])])
				check = int(joinNeighboors, 2)
				latticeOut.append(rule[check])
			elif i == 1:
				ESQESQESQ = (len(lattice) - 2)
				joinNeighboors = ''.join([str(lattice[ESQESQESQ]), str(lattice[ESQESQ]), str(lattice[ESQ]), str(lattice[i]), str(lattice[DIR]), str(lattice[DIRDIR]), str(lattice[DIRDIRDIR])])
				check = int(joinNeighboors, 2)
				latticeOut.append(rule[check])
			else:
				joinNeighboors = ''.join([str(lattice[ESQESQESQ]), str(lattice[ESQESQ]), str(lattice[ESQ]), str(lattice[i]), str(lattice[DIR]), str(lattice[DIRDIR]), str(lattice[DIRDIRDIR])])
				check = int(joinNeighboors, 2)
				latticeOut.append(rule[check])
		#guarda a lattice t=1, and so on, na lista updatedLattices para imprimir		
		updatedLattices.append(latticeOut)
		
		#iguala a lattice a latticeOut para continuar o resto dos timestamps
		lattice = latticeOut
		
	#serve para imprimir a lattice
	#para ver o resto de cada lattice, basta descomentar	
	printLattice(updatedLattices)
	
	#depois dos 202 timestamps, calcula o fitness da regra na lattice
	scores = checkFitness(updatedLattices, scores)
	
	#limpa a lista updatedLattices para ser utilizada na próxima lattice
	updatedLattices[:] = []
	return scores

def checkFitness(updatedLattices, scores):
	
	#por cada linha na lista updatedLattices:
	for i in range(len(updatedLattices)):
	
		#inicializa as var numZero e numOne para contar a maioria
		numZero = 0
		numOne = 0
		
		#se for a primeira linha:
		if (i == 0):
		
			#vai percorrer a primeira linha e
			#contar a quantidade de zeros ou uns que existem
			for j in range(len(updatedLattices[i])):
				if (updatedLattices[i][j] == 0):
					numZero += 1
				elif(updatedLattices[i][j] == 1):
					numOne += 1
			
			#chama a funcao checkMajority para obter a maioria
			#guarda o resultado na var majority
			majority = checkMajority(numZero, numOne)
			
		#se for a ultima linha:
		elif (i == len(updatedLattices)-1):
			for j in range(len(updatedLattices[i])):
				if (updatedLattices[i][j] == 0):
					numZero += 1
				elif(updatedLattices[i][j] == 1):
					numOne += 1
			
			#calcula o fitness com base na:
			#maioria obtida em cima
			#numZeros
			#numOnes
			#devolve o score
			scores = calcFitness(majority, numZero, numOne, scores)
	return scores

def checkMajority(numZero, numOne):
	majority = 0

	#se numOne for maior do que numZero
	#então maioria igual a 1
	if (numOne > numZero):
		majority = 1
		
	#caso contrario:
	#maioria é igual a 0
	else:
		majority = 0

	return majority

def calcFitness(majority, numZero, numOne, scores):
	
	#caso a maioria obtida em t=0 seja 0:
	if (majority == 0):
		score = float(numZero)/101
		
	#caso a maioria obtida em t=0 seja 1:
	elif (majority == 1):
		score = float(numOne)/101
		
	#guarda o score na lista de scores	
	scores.append(score)

	return scores

def doFitnessForRule(scores):

	#para calcular a media de scores de uma rule
	#somatorio dos valores na lista de ints
	#a dividir pelo tamanho da lista
	scoreOfRule = sum(scores)/float(len(scores))
	
	return scoreOfRule

def getTopRules(listRules): 

	#organiza top rules pelo fitness
	listRules = sorted(listRules,key=lambda x: x[0], reverse=True)
	
	#elimina tudo o resto que não é o top20
	del listRules [20:80] 
	
	#chama a funcao para escrever para ficheiro
	writeToFileTopRules(listRules)
	
	#chama a funcao para fazer crossover etc
	rearrangeRules(listRules)

def writeToFileTopRules(listRules):

	#abre o ficheiro ou cria caso não exista
	file = open("topRules.txt", "a")

	#para separar os valores por gerações
	file.write('----New Generation---\n')

	#por cada rule na lista de rules:
	for i, rule in enumerate (listRules):
	
		#para converter a rule de binario para decimal
		ruleDec = ''.join(str(x) for x in rule[1])
		ruleDec = ruleDec[::-1]
		ruleDec = int(ruleDec, 2)

		#para obter o score dessa regra
		score = rule[0]

		#escreve para ficheiro a rule e o score
		file.write('Rule: '+repr(str(ruleDec)))
		file.write(', Score of rule: '+repr(score)+'\n')

	#fechar o ficheiro
	file.close()

def rearrangeRules(listRules): 

	#porque estava a acrescentar [] a mais
	for i, rule in enumerate(listRules):
		listRules.pop(i)
		listRules.insert(i, rule[1])
	
	#chama a funcao para fazer crossover
	doCrossover(listRules)

def doCrossover(listRules):

	#incia contador para gerar os filhos
	#por cada volta, acrescenta dois filhos
	for i in range(21, 51): #51, 301
	
		#gera crossoverPoint aleatoriamente
		crossoverPoint = random.randint(0,128)
		
		#incia os dois filhos vazios
		filho1 = []
		filho2 = []
		
		#vai buscar aleatoriamente um pai e uma mãe
		pai = listRules[random.randint(0,19)] 
		mae = listRules[random.randint(0,19)]
		
		#de 0 a crossoverPoint
		for j in range(0,crossoverPoint):
			filho1.append(pai[j])
			filho2.append(mae[j])
		
		#de crossoverPoint até ao tamanho da rule
		for k in range(crossoverPoint,128):
			filho1.append(mae[k])
			filho2.append(pai[k])
		
		#guarda os filhos na lista de rules
		listRules.append(filho1)
		listRules.append(filho2)
	
	#chama a funcao para fazer mutações
	doMutation(listRules)

def doMutation(listRules):

	#define mutationRate com o valor 0.025
	mutationRate = 0.025

	#percorre os filhos, ou seja, de 21 a 80
	for i in range(21, 80):
	
		#por cada posicao em cada filho
		for index, item in enumerate(listRules[i]):
		
			#vai gerar um numero real aleatorio de 0 a 1
			r = random.uniform(0,1)
			
			#caso esse numero seja menor do que mutationRate
			if (r < mutationRate):
			
				#se o valor na posicao do filho for 1, passa a 0
				#se o valor na posicao do filho for 0, passa a 1
				if (item == 0):
					listRules[i][index] = 1
				elif (item == 1):
					listRules[i][index] = 0

	#chama a funcao correr a proxima geração
	nextGeneration(listRules)

def nextGeneration(listRules):
	print "\n ---- NEXT GENERATION ----\n"
	listLattices = generateLattice()
	updatedLattices = ruleOnLattice(listRules, listLattices)


def printLattice(updatedLattices):
	print "\n\n\n\n\n\n"
	
	#por cada uma das lattices
	for i in range(len(updatedLattices)):
	
		#vai percorrer cada posicao de uma lattice
		for j in range(len(updatedLattices[i])):
		
			#caso seja 0, imprime um espaço em branco
			#caso seja 1, imprime um ponto
			if (updatedLattices[i][j] == 0):
				sys.stdout.write(' ')
			elif(updatedLattices[i][j] == 1):
				sys.stdout.write('.')
		print ""

#para limpar a linha de comandos
os.system('clear')

print "---- 1ST GENERATION ----\n"

#para gerar as primeiras rules
listRules = generateInitRule()

#para gerar as primeiras lattices
listLattices = generateLattice()

#para chamar a funcao ruleOnLattice com base nas rules e lattices geradas
updatedLattices = ruleOnLattice(listRules, listLattices)