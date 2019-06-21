import math
import random

class GeneticAlgo:
    def __init__(self, obj_func, 
                 var_nums = 2, 
                 bound=[[0,1], [0,1]], 
                 chrom_num = 10,
                 mating_rate = 0.8,
                 mutation_rate = 0.05, 
                ):
        self.obj_func = obj_func
        self.mating_rate = mating_rate
        self.mutation_rate = mutation_rate
        self.chrom_num = chrom_num = 10
        
        self.var_nums = var_nums
        self.bound = bound
        #init randomly
        self.chroms = [[random.random()*(bound[1]-bound[0])+bound[0] for ii in range(chrom_num)] for bound in self.bound]
        self.chroms = [[self.chroms[jj][ii] for jj in range(len(self.chroms))] for ii in range(len(self.chroms[0]))]
        
        #best fitness chrom init to be the best chrom
        fitness = self.get_fitness()
#         print(fitness)
#         print(self.chroms)
        self.best_fitness = max(fitness)
        best_chrom_id = fitness.index(self.best_fitness)
        self.best_chrom = self.chroms[best_chrom_id].copy()
        
        
#     def obj_func(self, x):
#         return x[0]*math.sin(4*math.pi*x[0])+x[1]*math.sin(20*math.pi*x[1])
        
    #calculating the fitness using the object function
    def get_fitness(self):
        return [self.obj_func(chrom) for chrom in self.chroms]
    
    #select the chromosomes using RWS
    def rws(self, fitness):#roulette wheel selection
        f_min = min(fitness)
        f_max = max(fitness)
        #maybe the min and max is equal which will cause divided by zero error.
        if abs(f_min-f_max)>0.01:
            fitness = [(f-f_min)/(f_max-f_min) for f in fitness]

        fitness_norm = [f/sum(fitness) for f in fitness]
        s=0
        roulette_pro = [s+f for f in fitness_norm]#cumulating the probablity according the RWS algorithm
        
        chrom_selected=[]
        for jj in range(self.chrom_num):
            rand = random.random()
            chrom_id = 0
            for ii, pro in enumerate(roulette_pro):
                if pro>rand:
                    chrom_id=ii
                    break
            chrom_selected.append(chrom_id)
        #create the new chromosome using the indices selected by RWS algo
        self.chroms = [self.chroms[ii] for ii in chrom_selected]
    
    #mating
    def mating(self):
        #get mating flag according the mating rate.
        if_mating = [1 if random.random()<self.mating_rate else 0 for x in range(self.chrom_num)]
        
        mating_ids=[]
        for idx in range(len(if_mating)):
            if if_mating[idx]==1:
                mating_ids.append(idx)
        #create the mating position randomly. example: if the chromosome are [0.1, 0.2, 0.3] and 
        #[0.4, 0.5, 0.6], and the position is 0, so the chromsome will be cut and built to be 
        #[0.1,0.5,0.6] and [0.4, 0.2, 0.3]
        mating_positions=[random.randint(0, self.var_nums-2) for x in range(math.floor(len(mating_ids)/2))]
        for idx, pos in enumerate(mating_positions):
            chrom_x_id = mating_ids[idx*2]
            chrom_y_id = mating_ids[idx*2+1]
            
            chrom_x = self.chroms[chrom_x_id]
            chrom_y = self.chroms[chrom_y_id]
            chrom_x1 = chrom_x[:pos+1]
            chrom_x2 = chrom_x[pos+1:]
            chrom_y1 = chrom_y[:pos+1]
            chrom_y2 = chrom_y[pos+1:]
            chrom_x_new = chrom_x1+chrom_y2
            chrom_y_new = chrom_y1+chrom_x2
            
            self.chroms[chrom_x_id]=chrom_x_new
            self.chroms[chrom_y_id]=chrom_y_new
    
    #mutation: randomly change the value of chromosome
    def mutation(self):
        for chrom in self.chroms:
            for ii in range(self.var_nums):
                if random.random()<self.mutation_rate:
                    chrom[ii]=random.random()*(self.bound[ii][1]-self.bound[ii][0])+self.bound[ii][0]
    
    #iterate to search for the best chromosome. notice that the temparary best chromosome should be inserted to 
    #the self.chroms for creating better offspring chromosome. here i replace the worst chrom with the best chrom.
    def searching(self, iter_num=50):
        best_fitness_record=[]
        for ii in range(iter_num):
            fitness = self.get_fitness()
            best_fitness = max(fitness)
#             best_fitness_record.append(best_fitness)
            best_fitness_record.append(self.best_fitness)#saving the best_fitness for ploting
    
            if best_fitness>self.best_fitness:
                self.best_fitness = best_fitness
                best_chrom_id = fitness.index(best_fitness)
                self.best_chrom = self.chroms[best_chrom_id].copy()
            else:
                worst_fitness = min(fitness)
                worst_chrom_id = fitness.index(worst_fitness)
                self.chroms[worst_chrom_id] = self.best_chrom.copy()
                fitness[worst_chrom_id]=self.best_fitness
                
            self.rws(fitness)
            self.mating()
            self.mutation()
        return self.best_fitness, self.best_chrom, best_fitness_record