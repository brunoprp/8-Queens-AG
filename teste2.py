class Generation:
    def __init__(self, quant_gera, pop):
        self.quant_gera = quant_gera
        self.pop = pop

    def criar_roleta_selec(self):
        
        def prob_cruz_individos():
            maior_custo = 0
            lista_prob_individos = []
            prob = 0
            
            # Pegar o maior custo da populção para o calculo do percentual
            for i in range(len(self.pop)):
                custo= Custos(self.pop[i])
                custo_individo = custo.calculo_custo()              
                if custo_individo > maior_custo:
                    maior_custo = custo_individo

            # Criando um lista com o percentual de probabilidade 
            for j in range(len(self.pop)):
                custo= Custos(self.pop[j])
                custo_individo = custo.calculo_custo()
                prob = (custo_individo * 100) / maior_custo
                prob =  int(100 - prob)
                lista_prob_individos.append(prob)
            #Retorna as probabilidades de seleção de todos os individos e o valor maximo do range
            return lista_prob_individos, int(sum(lista_prob_individos)) 

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
        return roleta_prob_cruz, range_prob_cruz

    def cruzamento(self, roleta_prob_cruz, range_prob_cruz, prob_mut):
        nova_population = []
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
                    pai1 = self.pop[j]

                if index_p2 in roleta_prob_cruz[j]:
                    pai2 = self.pop[j]
            
            # funçao para garantir genis diferentes no individo cruzado
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
                return novo_genis
            
            # Cruzamneto de um ponto
            tam = len(self.pop[0])
            # Selecionado um ponto de cruzamento
            ponto = random.randint(2, tam-2) # Não seleciona as extremidades
            filho1, filho2 = [], []
        
        
            for p in range(0, ponto):
                if pai1[p] not in filho1:
                    filho1.append(pai1[p])
                    
                else:
                    filho1.append(novo_genis(pai1[p], filho1))
                                
                if pai2[p] not in filho2:
                    filho2.append(pai2[p])
            
                else:
                    filho2.append(novo_genis(pai2[p], filho2))

            for p in range(ponto, len(pai1)):
                if pai2[p] not in filho1:
                    filho1.append(pai2[p])
                    
                else:
                    filho1.append(novo_genis(pai2[p], filho1))

                if pai1[p] not in filho1:
                    filho2.append(pai1[p])
                    
                else:
                    filho2.append(novo_genis(pai1[p], filho1))              
            
            # aplica o operador de mutação
		    if random.random() <= prob_mut:
				gene1, gene2 = None, None
				while True:
					gene1 = random.randint(0, len(pai1))
					gene2 = random.randint(0, len(pai1))
					if gene1 != gene2:
						filho1[gene1], filho1[gene2] = filho1[gene2], filho1[gene1]
						filho2[gene1], filho2[gene2] = filho2[gene2], filho2[gene1]
						break

            # obtém o fitness dos pais e dos filhos
            f_fitnss_p1 = Custos(pai1)
            fitness_pai1 = f_fitnss_p1.obter_custo()

            f_fitnss_p2 = Custos(pai2)
            fitness_pai2 = f_fitnss_p2.obter_custo()

            f_fitnss_f1 = Custos(filho1)
            fitness_filho1 = f_fitnss_f1.obter_custo()

            f_fitnss_f2 = Custos(filho2)
            fitness_filho2 = f_fitnss_f2.obter_custo()
            
            if fitness_filho1 < fitness_pai1 or fitness_filho1 < fitness_pai2:
                if fitness_filho1 < fitness_pai1:
                    self.pop.remove(pai1)
                else:
                    self.pop.remove(pai2)
                self.pop.append(filho1)
            
            elif fitness_filho2 < fitness_pai1 or fitness_filho2 < fitness_pai2:
                if fitness_filho2 < fitness_pai1:
                    self.pop.remove(pai1)
                else:
                    self.pop.remove(pai2)
                self.pop.append(filho2)
            
            melhor_individo = self.pop[0][:]
            for ind in range(1, len(self.pop)):
                f_custo_melhor_ind = Custos(melhor_individo)
                custo_melhor_ind = f_custo_melhor_ind.obter_custo()
                f_custo_ind = Custos(self.po[ind])
                custo_ind = f_custo_ind.obter_custo()
                if custo_ind < custo_melhor_ind:
                    melhor_individo = self.pop[ind][:]

            print('Melhor indivíduo: %s\nCusto: %d' % (str(melhor_individuo), custo_melhor_ind)   