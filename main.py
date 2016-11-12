import os
from numpy import exp
import time
import random
import FlappyBirdClone.flappy as flappy

THRESHOLD = 90
MUT_THRESHOLD = 0.07
avgFitness = []
mutationProb = MUT_THRESHOLD
NUMBERGENES = 3

class Bird(object):

    def __init__(self):
        self.fitness = 1
        self.gene = [] #using 3 chromosomes
        self.flap = 0

    #2flapornot2flap
    def toflapornottoflap(self, inputs):
        self.flap = 0
        # print (inputs, self.gene)
        for i in zip (inputs, self.gene):
            self.flap += i[0] * i[1]
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
    for i in range (0, NUMBERGENES):
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
        mutationProb = mutationProb/1.1
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
    
    eliteNum = round(0.03*size) + 1 #so that it doesn't go to 0 if size < 100
    
    lowAvg = False
    avgFitness.append(get_average(pop, size))
    print(avgFitness)
    if check_improvement() == False:
        lowAvg = True

    for i in range (size):
        if i < eliteNum: # make flappy great again
            best = find_best(pop)
            print ("IL migliore ha: ", best.gene[0], best.gene[1], best.gene[2])
            newpop.append(best)
        elif lowAvg == True:
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
        pop[i+4] .fitness= ret[j+4]
        pop[i+5] .fitness= ret[j+5]
        # pop[i+6] .fitness= ret[j+6]
        # pop[i+7] .fitness= ret[j+7]
    return pop



from multiprocessing import Pool as ThreadPool
if __name__ == '__main__':
    from sys import argv
    randRange = [-300, 300]
    pop = big_bang (120, NUMBERGENES, randRange)
    pop = iterate_pop (pop)
    print(avgFitness)

    for i in range (0, int (argv[1])):
        if i == 50 and len(argv) == 4:
            print ("RALLENTO")
            flappy.FPS = 45
        print ("POP ", i+1)
        pop = create_new_population (pop, randRange)
        pop = iterate_pop (pop)
    print(avgFitness)
