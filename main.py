import os
from numpy import exp
import time
import random
import FlappyBirdClone.flappy as flappy

class Bird(object):

    def __init__(self):
        self.fitness = 1
        self.gene = [] #using 3 chromosomes
        self.flap = 0

    #2flapornot2flap
    def toflapornottoflap(self, inputs):
        self.flap = 0
        for i in zip (inputs, self.gene):
            self.flap += i[0] *  i[1] * random.randint (0, 100)
        # print ( 1 / (1 + exp (-self.flap / 100000)), self.flap)
        return 1 / (1 + exp (-self.flap / 100000))


def big_bang(n, sizeGene, randRange):
    # sizeGene = len of gene list
    # randRange = dimension of weight of genes
    #n = number of pidgeons
    pop = []
    for i in range(0, n):
        b = Bird()
        b.gene = [random.uniform (randRange[0], randRange[1]) for i in range(0, sizeGene)]
        pop.append (b)
    return pop

def have_the_sex (abird, bbird, mutationProb, randRange):
    child = Bird ()
    for i in range (3):
        if random.random () < mutationProb:
            child.gene.append (random.uniform (randRange[0], randRange[1]))
        if random.randint (0, 1):
            child.gene.append (abird.gene[i])
        else:
            child.gene.append (bbird.gene[i])

    return child

def create_new_population (pop, mutationProb, randRange):
    pool = list ()
    size = len (pop)
    for b in pop:
        for i in range (0, b.fitness):
            # create pool of elements to reproduce
            pool.append (b)

    newpop = list ()


    for i in range (size):
        b = pool[random.randint (0, size - 1)]
        a = pool[random.randint (0, size - 1)]
        while a == b:
            # you can't fap, b should be different from a
            ar = random.randint (0, len (pool) - 1)
            br = random.randint (0, len (pool) - 1)
            a = pool[ar]
            b = pool[br]
        newpop.append (have_the_sex (a, b, mutationProb, randRange))

    return newpop

def fitness (bird):
    travel, distance = flappy.main (bird)
    if distance == 0:
        distance = 0.001
    print (round (travel*10 - distance), " with this distance: ", distance, "with this travel: ", travel)
    return round (travel*10 - distance) 

def iterate_pop (pop):
    for i in range (0, len (pop), 6):
        j = 0
        pool = ThreadPool (6)
        lst = [pop[i], pop[i+ 1], pop [i+2], pop [i+3], pop [i+4], pop [i+5]]
        ret = pool.map (fitness, lst)
        pool.close ()
        pool.join ()
        pop[i] .fitness= ret[j]
        pop[i+1].fitness = ret[j+1]
        pop[i+2] .fitness= ret[j+2]
        pop[i+3] .fitness= ret[j+3]
        pop[i+5] .fitness= ret[j+5]
        pop[i+4] .fitness= ret[j+4]
    return pop



from multiprocessing import Pool as ThreadPool
if __name__ == '__main__':
    from sys import argv
    pop = big_bang (60, 3, [-100, 100])
    pop = iterate_pop (pop)

    for i in range (0, int (argv[1])):
        print ("POP ", i)
        pop = create_new_population (pop, 0.1, [-100, 100])
        pop = iterate_pop (pop)
