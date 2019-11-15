#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 20:16:46 2019

@author: bruno
"""

import random

class Individo: # Gera um individo aleatorio 
   def __init__(self, tamanho_tabuleiro, quanti_rainhas): #Construtor da classe
      self.tamanho_tabuleiro = tamanho_tabuleiro
      self.qunti_rainhas = quanti_rainhas
   def gera_individo(self): # Um individo é uma maneira de como as rainhas vão fica no tabuleiro!
      individo = []
      while len(individo) < self.qunti_rainhas: # Verifica se o quantiade de rainhas no tabuleiro
         xy = [] #Coordenada X e Y de uma rainha no tabuleiro
         xy.append(random.randint(0, self.tamanho_tabuleiro -1)) # Coordenada X aleatoria
         xy.append(random.randint(0, self.tamanho_tabuleiro -1)) # Coordenada Y aleatoria
         if xy in individo: # Verifica se a coordenada gerada já existe no tabuleiro 
            pass #Individo já existente!
            #print("Individo já existente!")
         else:
            individo.append(xy)
      return individo # Retorna uma lista das posições das rainhas no tabuleiro

class Population: #Gera populção inicial com varios individos (Possiveis Solucões)
   def __init__(self, tam_pop): #Constratutor de classe
      self.tam_pop = tam_pop
      self.pop = []
   def gera_pop(self, tamanho_tabuleiro, quanti_rainhas):
      individo = Individo(tamanho_tabuleiro, quanti_rainhas) # Instacinado a classe Individo
      for i in range(self.tam_pop): # Gera a quantidade da pupulação
         self.pop.append(individo.gera_individo()) # Chamando o metdo de gerar individo
      return self.pop  #Retorna populçaõ inicial
  
class Custos: # Função fitness verifica quantas rainhas estão se cruzando 

    def calculo_custo(self, individo):
      cont = 0
      lista_verificada = []
      
      # Verifica se existe indice iguais se tiver então as rainhas estão se cruzando nas linhas ou colunas
      def calculo_custo_LC(individo): 
         lista_x = []
         lista_y = []
         cont = 0
         # Pegando os valores das cordendas x e y
         for i in range(len(individo)):
            pop = individo[i]
            lista_x.append(pop[0])
            lista_y.append(pop[1])
         
         # Verficando quantos numeros repeditos existe nas cordenas x e Y  
         for j in range(0,len(lista_x)):
            soma_x = lista_x.count(j)
            soma_y = lista_y.count(j)
            if soma_x == 0 or soma_x == 1:
               soma_x = 0
            if soma_y == 0 or soma_y == 1:
               soma_y = 0
            if soma_x > 0:
               soma_x = soma_x-1
            if soma_y > 0:
               soma_y = soma_y-1
            cont = cont+(soma_x+soma_y) 
         return cont # Retorna a qunatidade de rainhas se cruzando nas linhas e colunas
          
      custoLC = calculo_custo_LC(individo) # Resultados que quntas rainhas se cruzam nas linhas e colunas
      
      # função para frificar se as rainhas já foram ferificadas
      def verifica_lc(lista1, lista2):
        verifica = False
        if lista1[0] == lista2[0] or lista1[1] == lista2[1]:
           verifica = True
        return verifica
        
      ## Calculando o custo das diagonais (quntas rainhas se cruzam nas diagonais)
      for i in range(0, len(individo)):
         lista_temp =  individo[:]        
         posi = individo[i]
         lista_temp.pop(i)
         for j in range(0, len(lista_temp)):
            lista1 = []
            
            verifica = lista_temp[j]
            
            lista1.append(verifica)
            lista1.append(posi)
            
            verfica_colunas = verifica_lc(posi, verifica)
            
            if lista1 in lista_verificada or verfica_colunas == True:
                pass #já foi verificado / ta na mesma linha ou coluna!
               # print("já foi verificado / ta na mesma linha ou coluna!")

            elif ( posi[0] + posi[1]) == (verifica[0] + verifica[1])  or (posi[0] - posi[1]) == (verifica[0] - verifica[1]) :
                lista2 = []
                lista2.append(posi)
                lista2.append(verifica)
                lista_verificada.append(lista2)              
                cont+=1       
      return  custoLC+cont # Retorna a qunatiade de rainhas que estão se cruzando
  
class Generation:
    def __init__(self, quant_gera, pop):
        self.quant_gera = quant_gera
        self.pop = pop

    def criar_roleta_selec(self):
        obj_custos = Custos()
        
        def prob_cruz_individos():
            maior_custo = 0
            lista_prob_individos = []
            prob = 0
            
            # Pegar o maior custo da populção para o calculo do percentual
            for i in range(len(self.pop)):
                custo= obj_custos.calculo_custo(self.pop[i])        
                if custo > maior_custo:
                    maior_custo = custo

            #print(maior_custo)
            # Criando um lista com o percentual de probabilidade 
            for j in range(len(self.pop)):
                custo_individo = obj_custos.calculo_custo(self.pop[j])
                prob = (custo_individo * 100) / maior_custo
                prob =  int(100 - prob)
                lista_prob_individos.append(prob)
            #Retorna as probabilidades de seleção de todos os individos e o valor maximo do range
            return lista_prob_individos, int(sum(lista_prob_individos)) 

        # Cria a roleta com range de numeros para cada individo de acordo com a aptidão
        def roleta(lista_prob):
            roleta = []
            cont = 0
            for i in range(0, len(lista_prob)):
                range_prob_individo = lista_prob[i]                   
                list_range_prob_indi = []
                for j in range(cont, cont + range_prob_individo):
                    list_range_prob_indi.append(j)
                    cont += 1
                roleta.append(list_range_prob_indi)
            return roleta
       
        
        lista_prob_cruz_individos, range_prob_cruz = prob_cruz_individos()
        roleta_prob_cruz = roleta(lista_prob_cruz_individos)
        return roleta_prob_cruz, range_prob_cruz # Retorna a roleta e o tamnho do range
    

    def cruzamento(self, roleta_prob_cruz, range_prob_cruz, prob_mut):
        nova_population = self.pop[:]
        obj_custos = Custos()
        # funçao para garantir genis diferentes no individo cruzado (Posições repetidas no taboleio)
        def novo_genis(genis, filho):   
            while True:
                novo_genis = []
                x = random.randint(0, 7)
                y = random.randint(0, 7)
                novo_genis.append(x)
                novo_genis.append(y)
                #print("aqui")
                if novo_genis != genis and novo_genis not in filho:
                        break
            return novo_genis # Retorna um novo genis diferente
        
        
        for i in range(0, self.quant_gera):
            index_p1, index_p2 = None, None
            pai1, pai2 = [], []
            
            # selecionando os individos de acordo com a probabiliade de cruzamento
            while True:
                index_p1 = random.randint(0, range_prob_cruz-1)
                index_p2 = random.randint(0, range_prob_cruz-1)
                if index_p1 != index_p2:
                    break
            
            for j in range(0, len(roleta_prob_cruz)):
                if index_p1 in roleta_prob_cruz[j]:
                    pai1 = nova_population[j]

                if index_p2 in roleta_prob_cruz[j]:
                    pai2 = nova_population[j]
            
            # Cruzamneto de um ponto
            tam = len(nova_population[0])
            # Selecionado um ponto de cruzamento
            ponto = random.randint(0, tam-1) # Não seleciona as extremidades
            filho1, filho2 = [], []
            for p in range(0, ponto):
                if pai1[p] not in filho1: # Verifica se já existe o genis (se ja existe a Rainha )
                    filho1.append(pai1[p])
                    
                else:
                    filho1.append(novo_genis(pai1[p], filho1)) # Pega um novo genis valido (Rainha) 
                                
                if pai2[p] not in filho2: # Verifica se já existe o genis (se ja existe a Rainha )
                    filho2.append(pai2[p])
            
                else:
                    filho2.append(novo_genis(pai2[p], filho2)) # Pega um novo genis valido (Rainha)

            for p in range(ponto, len(pai1)):
                if pai2[p] not in filho1:
                    filho1.append(pai2[p])
                    
                else:
                    filho1.append(novo_genis(pai2[p], filho1))

                if pai1[p] not in filho1:
                    filho2.append(pai1[p])
                    
                else:
                    filho2.append(novo_genis(pai1[p], filho1))
            
            # Aplica o operador de mutação
            if random.random() <= prob_mut:
                gene1, gene2 = None, None
                while True:
                    gene1 = random.randint(0, len(pai1)-1)
                    gene2 = random.randint(0, len(pai1)-1)
                    if gene1 != gene2:
                        filho1[gene1], filho1[gene2] = filho1[gene2], filho1[gene1]
                        filho2[gene1], filho2[gene2] = filho2[gene2], filho2[gene1]
                        break
                    
            # obtém o fitness dos pais e dos filhos
            fitness_pai1 = obj_custos.calculo_custo(pai1)
            fitness_pai2 = obj_custos.calculo_custo(pai2)
            fitness_filho1 = obj_custos.calculo_custo(filho1)
            fitness_filho2 = obj_custos.calculo_custo(filho2)
            
            # Trocar o filho pelo pai se o filho for melhor
            if fitness_filho1 < fitness_pai1 or fitness_filho1 < fitness_pai2:
               # print("fitness_filho1 melhor que pai1 ou pai2")
                if fitness_filho1 < fitness_pai1:
                    nova_population.remove(pai1)
                else:
                    nova_population.remove(pai2)
                nova_population.append(filho1)           
            elif fitness_filho2 < fitness_pai1 or fitness_filho2 < fitness_pai2:
                #print("fitness_filho2 melhor que pai1 ou pai2")
                if fitness_filho2 < fitness_pai1:
                    nova_population.remove(pai1)
                else:
                    nova_population.remove(pai2)
                nova_population.append(filho2)
            
            #Verificar o melhor individo a cada geração
            melhor_individo = nova_population[0][:]
            custo_melhor_ind = obj_custos.calculo_custo(melhor_individo)            
            for ind in range(1, len(nova_population)):                
                custo_ind = obj_custos.calculo_custo(nova_population[ind])                
                if custo_ind < custo_melhor_ind:
                    #print("trucou o melhor custo")
                    melhor_individo = nova_population[ind][:]
                    custo_melhor_ind = obj_custos.calculo_custo(melhor_individo)
                    #print(custo_melhor_ind)

            print("Melhor indivíduo: %s\nCusto: %d" % (str(melhor_individo), custo_melhor_ind))
        return nova_population # Retorna a populçao depois do cruzamento

obj_pop = Population(tam_pop = 1000) # Cria um objeto da classe Population com 1000 individos
pop = obj_pop.gera_pop(8, 8) # Gerar uma população de 1000 com 8 rainhas e o tabuleiro 8x8
#pop_teste= pop[:]

obg_gera = Generation(quant_gera = 1000, pop= pop) #Cria um objeto da classe Generation com uma geração 1000

roleta_prob_cruz, range_cruz = obg_gera.criar_roleta_selec() # Roleta de probabilidade e o tamanho range
pop_teste = obg_gera.cruzamento(roleta_prob_cruz,range_cruz, prob_mut = 0.1)

#print(obg_gera.criar_roleta_selec())
#obj_custos = Custos()
#print(obj_custos.calculo_custo(pop[6]))


############# Verfifica o melhor invido depois das gerações#####################
obj_custos = Custos()
melhor_custo = obj_custos.calculo_custo(pop_teste[0]) 
for i in range(1, len(pop_teste)):
    custo_ind = obj_custos.calculo_custo(pop_teste[i])
    if custo_ind < melhor_custo:
        melhor_custo = custo_ind
        melhor_individo = pop_teste[i][:]

print(melhor_custo) 
print(melhor_individo)
    
