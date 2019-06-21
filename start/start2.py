import math
#import matplotlib.pyplot as plt

import sys
sys.path.append('../imple/')
from GeneticClass import GeneticAlgo

def obj_func(x):
    return 1/(x[0]**2+x[1]**2+x[2]**2+x[3]**2+1)

genetic = GeneticAlgo(obj_func=obj_func, var_nums=4, 
                      bound=[[-5, 5], [-5, 5], [-5, 5], [-5, 5]], chrom_num = 20, 
                      mating_rate=0.88, mutation_rate=0.2)

best_fitness, best_chrom, best_fitness_record = genetic.searching(iter_num=1000)
print(best_fitness, best_chrom)

#iter_th = range(len(best_fitness_record))
#plt.plot(iter_th, best_fitness_record)
#plt.show()