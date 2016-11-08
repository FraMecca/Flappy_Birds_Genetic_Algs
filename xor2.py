""" 2-input XOR example """
from __future__ import print_function

import os

from neat import nn, population, statistics, parallel

# Network inputs and expected outputs.
xor_inputs = [[0],
              [1],
              [2],
              [3],
              [4],
              [5],
              [6],
              [8]]
xor_outputs = [0, 1, 4, 9, 16, 25, 36, 64]

import time
import FlappyBirdClone.flappy as flappy

def eval_fitness(g):
    time_init = time.time()
    net = nn.create_feed_forward_phenotype(g)
    flappy.main(net)
    # output = net.serial_activate(inputs)

    # When the output matches expected for all inputs, fitness will reach
    # # its maximum value of 1.0.
    # print (sum_square_error, "--> ERROR")
    # g.fitness = time.time() - time_init
    return time.time() - time_init

# local_dir = os.path.dirname(__file__)
local_dir = "/home/user/git_mio/neat"
config_path = os.path.join(local_dir, 'xor2_config')
pe = parallel.ParallelEvaluator(6, eval_fitness)
pop = population.Population(config_path)
pop.run(pe.evaluate, 6000)


# Log statistics.
# statistics.save_stats(pop.statistics)
# statistics.save_species_count(pop.statistics)
# statistics.save_species_fitness(pop.statistics)

print('Number of evaluations: {0}'.format(pop.total_evaluations))

# Show output of the most fit genome against training data.
winner = pop.statistics.best_genome()
print('\nBest genome:\n{!s}'.format(winner))
print('\nOutput:')
# at this point, just create a net using the winner and make it compute the solution with its parameters
winner_net = nn.create_feed_forward_phenotype(winner)
for inputs, expected in zip(xor_inputs, xor_outputs):
    output = winner_net.serial_activate(inputs)
    print("expected {0:1.5f} got {1:1.5f}".format(expected, output[0] * 100))

while (1):
    print ("dammi un numero")
    n = input ()
    print (winner_net.serial_activate ([int (n)]) [0] * 100)
