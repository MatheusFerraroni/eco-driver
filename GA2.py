import numpy as np
import threading
import time
import sys
import codecs
import json




"""

Classe do Elemento de cada solucao

Dependendo das abordagens e alteracoes vai ser bom ter isso separado em uma classe no futuro



"""
class element:

    def __init__(self, idd, geracao, genome):
        self.idd = idd
        self.geracao = geracao
        self.genome = genome
        self.score = None


    def __repr__(self):
        return "(id={},geracao={},score={:.20f})".format(self.idd, self.geracao,self.score)


"""

Classe responsavel por controlar todo o funcionamento do algoritmo genetico
Eh preciso fazer override dos metodos random_genome() e evaluate(). (pode ser feito diretamente ou com as funcoes set_evaluate() e set_random_genome())

"""
class GeneticAlgorithm:


    """
    
    define parametros iniciais e cria populacao aleatoria
    os parametros podem ser alterados pelos setters

    """
    def __init__(self, random_genome_func):
        self.population = []
        self.historic = []
        self.mutation_rate = 0
        self.population_size = 50
        self.iteration_limit = 5
        self.elements_created = 0
        self.crossover_type = 0
        self.best_element_total = None
        self.max_possible_score = float('inf')
        self.iteration_counter = 0
        self.stop_criteria_type = 0
        self.probs_type = 0
        self.use_threads = False
        self.crossover_rate = 0.5
        self.cut_half_population = False

        self.replicate_best = 0 # amount of best elements to replicate between generations
        self.set_random_genome(random_genome_func)


    def get_config(self):
        o = {}

        o["mutation_rate"] = self.mutation_rate
        o["population_size"] = self.population_size
        o["iteration_limit"] = self.iteration_limit
        o["elements_created"] = self.elements_created
        o["crossover_type"] = self.crossover_type
        o["max_possible_score"] = self.max_possible_score
        o["iteration_counter"] = self.iteration_counter
        o["stop_criteria_type"] = self.stop_criteria_type
        o["probs_type"] = self.probs_type
        o["crossover_rate"] = self.crossover_rate
        o["cut_half_population"] = self.cut_half_population
        o["replicate_best"] = self.replicate_best

        return o


    """
    
    executa o loop principal do algoritmo genetico

    """
    def run(self):

        print("[GA] Evolução iniciada")


        self.time_start = time.time()

        if len(self.population)==0:
            self.create_initial_population()

        while self.check_stop():
            self.calculate_score() # PRIMEIRO: Definir score
            self.population.sort(key=lambda x: x.score, reverse=True) # SEGUNDO: Ordenar pelo score

            if self.best_element_total==None:
                self.best_element_total = self.population[0]

            if self.population[0].score > self.best_element_total.score: # salva melhor elemento
                self.best_element_total = self.population[0]

            self.do_log()
            print("[GA]  Geração: {}, Best geral: {:.20f}, Best Atual: {:.20f}, Média: {:.20f}".format(self.iteration_counter,self.best_element_total.score,self.historic[-1]["best"],self.historic[-1]["avg"]))


            if self.cut_half_population: # Desativado por padrão. Pode ser util para ajudar a melhoarar a evolução
                self.population = self.population[0:len(self.population)//2] # Descarta pior metade da populacao. 

            self.iteration_counter +=1
            
            self.new_population()





        self.time_end = time.time()

        print("[GA] Evolução finalizada. Tempo total: {:.2f} segundos".format(self.time_end-self.time_start))
        return self.best_element_total


    """

    Cria uma nova populacao

    """
    def new_population(self):

        probs = self.get_probs()

        newPop = []

        best_replicator = int(self.population_size*self.replicate_best)

        while len(newPop)<self.population_size-best_replicator:
            parents = []
            try:
                parents = np.random.choice(self.population, size=2, p=probs) #seleciona parents
            except Exception as e:
                print("[GA] ERRO_POP", self.population)
                print("[GA] probs", probs)
                raise

            if parents[0].score<parents[1].score: # garantirmos que o parents[0] sempre tem o elemento melhor. assim as funcoes de crossover sempre vao receber ele no primeiro parametro
                parents = parents[::-1] # reverse o array

            new_element = element(self.elements_created, self.iteration_counter, self.crossover(parents[0].genome, parents[1].genome))

            new_element.genome = self.active_mutate(new_element.genome)
            newPop.append(new_element)
            self.elements_created += 1

        for i in range(best_replicator):
            newPop.append(self.population[i])

        self.population = newPop

    """

    Retorna um array com o tamanho de len(self.population) onde cada posição desse array indica a chance de um elemento da população ser selecionado (soma do array deve ser == 1)
    
    """
    def get_probs(self):
        if self.probs_type == 0:
            return self.probs_roulette()
        elif self.probs_type == 1:
            return self.probs_equal()


    """

    Todos os elementos tem a mesma chance de ser selecionado

    """
    def probs_equal(self):
        return [1/len(self.population)]*len(self.population)


    """
    
    Elementos com score maior tem mais chance de serem selecionados

    """
    def probs_roulette(self):
        probs = [0]*len(self.population) # gera array de probs para selecionar parents
        for i in range(len(probs)):
            probs[i] = self.population[i].score
        div = sum(probs)

        if div>0:
            for i in range(len(probs)):
                probs[i] /= div
        else: # Se nenhuma solução consegue resolver nada, retorna chance igual para todos os elementos
            probs = self.probs_equal()
        return probs


    """
    
    Salva os logs da geracao na variavel self.historic

    """

    def gen_to_array(self, gen):
        if type(gen)==np.ndarray:
            ret = []
            for i in range(len(gen)):
                ret.append(self.gen_to_array(gen[i]))
            return ret
        return gen

    def do_log(self):

            score_geracao_medio = 0
            score_geracao_max = float('-inf')
            score_geracao_min = float('inf')
            for i in range(len(self.population)):
                score_geracao_medio += self.population[i].score
                score_geracao_min = min(score_geracao_min, self.population[i].score)
                score_geracao_max = max(score_geracao_max, self.population[i].score)
            score_geracao_medio /= len(self.population)

            todos_genomes = []
            for i in range(len(self.population)):
                todos_genomes.append(self.gen_to_array(self.population[i].genome))


            self.historic.append({"geracao":self.iteration_counter,
                "max":score_geracao_max,
                "min":score_geracao_min,
                "avg":score_geracao_medio,
                "best":self.best_element_total.score,
                "best_genome":self.gen_to_array(self.best_element_total.genome),
                # "todos_genomes":todos_genomes
                })
               



    """

    Checagem do stop criteria

    """
    def check_stop(self):
        ret = None
        if self.stop_criteria_type==0:
            ret = self.stop_criteria_double()
        elif self.stop_criteria_type==1:
            ret = self.stop_criteria_iteration()
        elif self.stop_criteria_type==2:
            ret = self.stop_criteria_score()


        return ret


    """

    Checa por limite de iteracao e max_score

    """
    def stop_criteria_double(self):
        s = self.population[0].score
        if s==None:
            s = 0
        return self.iteration_counter<self.iteration_limit or s>=self.max_possible_score


    """

    Checa apenas por limite de iteração

    """
    def stop_criteria_iteration(self):
        return self.iteration_counter<self.iteration_limit


    """

    Checa apenas por score máximo

    """
    def stop_criteria_score(self):
        s = self.population[0].score
        if s==None:
            s = 0
        return s>=self.max_possible_score


    def set_replicate_best(self, e):
        if e<0 or e>1:
            raise Exception("Value must be between 0 and 1.")
        self.replicate_best = e

    def set_probs_type(self, e):
        self.probs_type = e

    def set_cut_half_population(self, e):
        self.cut_half_population = e

    def set_max_score(self, e):
        self.max_possible_score = e

    def set_iteration_limit(self, e):
        self.iteration_limit = e

    def set_population_size(self, e):
        self.population_size = e

    def set_mutation_rate(self, e):
        self.mutation_rate = e

    # Faz o override da funcao evaluate
    def set_evaluate(self, e):
        self.evaluate = e

    # Faz o override da funcao random_genome
    def set_random_genome(self, e):
        self.random_genome = e

    def set_mutate(self, e):
        self.mutate = e

    def set_stop_criteria_type(self, e):
        self.stop_criteria_type = e

    def threads(self, e):
        self.use_threads = e

    # gera uma populacao nova
    # o metodo random_genome precisa ter sido override
    def create_initial_population(self):
        self.population = []
        for _ in range(self.population_size):
            self.population.append(element(self.elements_created, 0, self.random_genome()))
            self.elements_created += 1


    # set do crossover type.
    # atualmente aceita 3 valores
    def set_crossover_type(self, e):
        self.crossover_type = e

    def set_crossover_rate(self, e):
        self.crossover_rate = e


    # chama o metodo de crossover que esta sendo utilizado
    def crossover(self, genA, genB):
        return self.crossover_uniform(genA, genB)


    # CROSSOVER (Uniform Crossover)
    def crossover_uniform(self, genA, genB):
        if type(genA)==np.ndarray:
            ret = []
            for i in range(len(genA)):
                ret.append(self.crossover_uniform(genA[i], genB[i]))
            return np.array(ret, dtype=object)
        if np.random.random()<0.5:
            return genA
        else:
            return genB




    #chama a funcao que calcula o score para cada elemento da populacao
    def calculate_score(self):
        print("[GA]  Iniciando avaliação de scores")
        for e in self.population:
            e.score = self.evaluate(e.genome, "_"+str(e.geracao)+"_"+str(e.idd)+".out.xml")
            print("[GA]  Avaliado: "+str(e))
        print("[GA]  Completo avaliação de scores")


    # a mutacao troca o valor dos bits entre 0 e 1
    def active_mutate(self,gen):
        return self.mutate(gen)





    # Precisa ser override
    # Gera um genoma completamente aleatorio (Usado principalmente na primeira geracao)
    def random_genome(self):
        raise Exception("Should be override")


    # esse metodo eh obrigatoriamente override
    # calcula o fitness
    def evaluate(self):
        raise Exception("Should be override")


    # esse metodo eh obrigatoriamente override
    # faz a mutacao de uma posicao do genoma
    def mutate(self):
        raise Exception("Should be override")