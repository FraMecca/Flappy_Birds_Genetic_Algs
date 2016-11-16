import os
from math import exp
import time
import random
import FlappyBirdClone.flappy as flappy
from multiprocessing import cpu_count,  Pool as ThreadPool

THRESHOLD = 70
MUT_THRESHOLD = 0.07
avgFitness = []
mutationProb = MUT_THRESHOLD

class Bird(object):

    def __init__(self):
        self.fitness = 1
        self.gene = [] #using 3 chromosomes
        self.flap = 0 
    #2flapornot2flap
    def toflapornottoflap(self, inputs):
        self.flap = 0
        for i in zip (inputs, self.gene):
            self.flap += i[0] *  i[1] #* random.randint (0, 100)
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

def have_the_sex (abird, bbird, randRange):
    child = Bird ()
    for i in range (2):
        if random.random () < mutationProb:
            child.gene.append (random.uniform (randRange[0], randRange[1]))
        if random.randint (0, 1):
            child.gene.append (abird.gene[i])
        else:
            child.gene.append (bbird.gene[i])

    return child

# for elitism
def find_best(pop):
    bestFit = 0
    for b in pop:
        if b.fitness > bestFit:
            best = b
            bestFit = best.fitness
            pop.pop(pop.index(b))# ohgodwhy
    return best

# for average improvement
def get_average(pop, n):
    avg = 0
    for b in pop:
        avg += b.fitness
    avg = avg / n
    return avg

def check_improvement():
    global mutationProb
    if len(avgFitness) == 1:
        return True
    diff = avgFitness[-1] - avgFitness[-2]
    if diff < (0.005 * avgFitness[-2]):
        if avgFitness[-1] < THRESHOLD:
            mutationProb = MUT_THRESHOLD
            print('MUTATION', mutationProb)
            return False
        elif avgFitness[-1] > THRESHOLD:
            mutationProb = mutationProb*1.1
            print('MUTATION', mutationProb)
    elif mutationProb > MUT_THRESHOLD:
        mutationProb = MUT_THRESHOLD
        print('MUTATION', mutationProb)

    return True 

def create_new_population (pop, randRange):
    global avgFitness
    pool = list ()
    size = len (pop)
    for b in pop:
        for i in range (0, b.fitness):
            # create pool of elements to reproduce
            pool.append (b)

    newpop = list ()

    eliteNum = round(0.04*size) + 1 #so that it doesn't go to 0 if size < 100

    lowAvg = False
    avgFitness.append(get_average(pop, size))
    print(avgFitness)
    if check_improvement() == False:
        lowAvg = True

    for i in range (size):
        if i < size - eliteNum: 
            if lowAvg == True:
                print('newbreed!')
                newbreed = big_bang(size - eliteNum, 3, randRange)
                newpop.extend(newbreed)
                break
            else:
                b = pool[random.randint (0, size - 1)]
                a = pool[random.randint (0, size - 1)]
                while a == b:
                    # you can't fap, b should be different from a
                    ar = random.randint (0, len (pool) - 1)
                    br = random.randint (0, len (pool) - 1)
                    a = pool[ar]
                    b = pool[br]
                newpop.append (have_the_sex (a, b, randRange))
        else: #make flappy great again
            best = find_best(pop)
            print ("IL migliore ha: ", best.gene[0], best.gene[1])
            newpop.append(best)
    return newpop

def fitness (bird):
    import time

    start = time.time()
    travel, distance = flappy.main (bird)
    # if distance == 0:
        # distance = 0.001
    # print (round (travel*10 - distance), " with this distance: ", distance, "with this travel: ", travel)
    # return round (travel*10 - distance) 
    t = round((time.time() - start)*100)
    # print(t)
    return t

def iterate_pop (pop):
    ncpu = cpu_count()
    for i in range (0, len (pop), ncpu):
        j = 0
        lst = []
        pool = ThreadPool (ncpu)
        for j in range(0, ncpu - 1):
            if i+j < len(pop):
                lst.append(pop[i+j])
        ret = pool.map (fitness, lst)
        pool.close ()
        pool.join ()
        for j in range(0, ncpu - 1):
            if i+j < len(pop):
                pop[i+j].fitness= ret[j]
    return pop



if __name__ == '__main__':
    from sys import argv
    print("Press Ctrl-C to stop.")
    randRange = [-90, 90]
    flappy.change_fps(int(argv[2]))
    pop = big_bang (int(argv[1]), 2, randRange)
    pop = iterate_pop (pop)
    print(avgFitness)
    for i in range (0, int (argv[1])):
        print ("POP ", i+1)
        pop = create_new_population (pop, randRange)
        pop = iterate_pop (pop)
    print(avgFitness)
