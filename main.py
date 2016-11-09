import os

from neat import nn, population, statistics, parallel

# import time
import FlappyBirdClone.flappy as flappy

def eval_fitness(g):
    # time_init = time.time()
    net = nn.create_feed_forward_phenotype(g)
    pipeCnt, dist1, dist2, travel = flappy.main(net)
    # output = net.serial_activate(inputs)

    # When the output matches expected for all inputs, fitness will reach
    # # its maximum value of 1.0.
    # print (sum_square_error, "--> ERROR")
    # g.fitness = time.time() - time_init
    t = pipeCnt * 10 - (dist1 / 50 + dist2 / 50) * travel  + travel * 1
    print(t)
    return t

local_dir = os.path.dirname('../')
config_path = os.path.join(local_dir, 'main_config')
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
