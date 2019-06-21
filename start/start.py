import math
#import matplotlib.pyplot as plt

import sys
sys.path.append('../imple/')
from GeneticClass import GeneticAlgo

def obj_func(x):
    return x[0]*math.sin(4*math.pi*x[0])+x[1]*math.sin(20*math.pi*x[1])

genetic = GeneticAlgo(obj_func=obj_func, var_nums=2, 
                      bound=[[-3, 12], [4,5.8]], chrom_num = 20, 
                      mating_rate=0.88, mutation_rate=0.2)

best_fitness, best_chrom, best_fitness_record = genetic.searching(iter_num=1000)
print(best_fitness, best_chrom)

#iter_th = range(len(best_fitness_record))
#plt.plot(iter_th, best_fitness_record)
#plt.show()