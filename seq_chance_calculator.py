# Sequential chance brute force calculator
# Methods: mcm(monte carlo method), bruteforce(calc all combinations)
# Calculates the chance of k or more sequential rolls occuring in n rolls
# 
# Author: tadyen


import numpy as np

class user_input_form:
    supported_calc_methods = {  'bruteforce',
                                'mcm'
                            }
    def __init__(self, calc_method, p_chance, k_rolls, N_rolls, N_mcm):
        assert(type(calc_method)==str)
        self.calc_method = calc_method

        assert(type(p_chance)==float)
        self.p_chance = p_chance

        assert(type(N_rolls)==int)
        self.N_rolls = N_rolls
        
        assert(type(k_rolls)==int)
        self.k_rolls = k_rolls

        assert(type(N_mcm)==int)
        self.N_mcm = N_mcm
        return

    def ask_calc_method(self):
        print(r"Input calculation method: 'bruteforce', 'mcm'")
        self.calc_method = input()
        if(self.calc_method not in self.supported_calc_methods):
            print("Method is not supported")
            return False
        return True

    def ask_p_chance(self):
        print(r"Input probability of roll success (between 0 and 1)")
        try:
            self.p_chance = float(input())
        except:
            print("Input must be an float")
            return False

        if(self.p_chance<0 or self.p_chance>1):
            print("Chance must be between 0 and 1")
            return False
        return True
        
    def ask_N_rolls(self):
        print(r"Input number of total rolls")
        try:
            self.N_rolls = int(input())
        except:
            print("Input must be an int")
            return False

        if(self.N_rolls <= 0):
            print("Rolls must be greater than 0")
            return False
        return True

    def ask_k_rolls(self):
        print(r"Input minimum number of sequential rolls")
        try:
            self.k_rolls = int(input())
        except:
            print("Input must be an int")
            return False

        if(self.k_rolls <= 0):
            print("Rolls must be greater than 0")
            return False
        elif(self.k_rolls>self.N_rolls):
            print("Sequential rolls must not be greater than total rolls")
            return False
        return True

    def ask_N_mcm(self):
        print(r"Input number of runs for the MCM")
        try:
            self.N_mcm = int(input())
        except:
            print("Input must be an int")
            return False
        if(self.N_mcm <= 0):
            print("MCM runs must be greater than 0")
            return False
        return True
    
    @staticmethod
    def ask_form():
        form = user_input_form('',0.0,0,0,0)
        loop_cond = False
        while not loop_cond: loop_cond = form.ask_calc_method()
        loop_cond = False
        while not loop_cond: loop_cond = form.ask_p_chance()
        loop_cond = False
        while not loop_cond: loop_cond = form.ask_N_rolls()
        loop_cond = False
        while not loop_cond: loop_cond = form.ask_k_rolls()
        if form.calc_method == 'mcm':
            loop_cond = False
            while not loop_cond: loop_cond = form.ask_N_mcm()
        return form

def calculate_seq_chance(input_form):
    def bruteforce(p_chance, k_rolls, N_rolls):
        print('Bruteforce calc: p={p}, k={k}, N={n}'.format(p=p_chance,k=k_rolls,n=N_rolls))
        # Creating all the probabilities for the bruteforce calculation
        N = 2**N_rolls
        permutation=""
        permute_success = False
        permute_chance = float(0)
        total_chance = float(0)
        ii=0
        while(ii<N):
            permutation=bin(ii)[2:].zfill(N_rolls)
            permute_success = check_permute_success(permutation,k_rolls,'GE')
            if(permute_success == True):
                permute_chance = calc_permute_chance(permutation, p_chance)
                #print('Permutation: {binstr}'.format(binstr=permutation))
                #print('permute chance: {x}'.format(x=permute_chance))
                total_chance += permute_chance
            ii+=1
        return total_chance
        
    
    def mcm(p_chance, k_rolls, N_rolls, N_mcm):
        def generate_permutation(p_chance,N_rolls):
            permutation = bin(0)[2:].zfill(N_rolls)
            char_list = list(permutation)
            ii=0
            while(ii<N_rolls):
                if(np.random.rand()<p_chance):
                    char_list[-ii-1] = '1'
                ii+=1
            permutation = "".join(char_list)
            return permutation

        print('MCM calc: p={p}, k={k}, N={n}, N_runs={mcm}'.format(p=p_chance,k=k_rolls,n=N_rolls,mcm=N_mcm))
        ii=0; successes=0
        while(ii<N_mcm):
            permutation = generate_permutation(p_chance,N_rolls)
            if(check_permute_success(permutation,k_rolls,'GE')==True):
                successes+=1
            ii+=1
        return (float(successes)/float(N_mcm))

    def check_permute_success(input_bin_str, k_rolls, compare_mode):
        #compare consequtive successes (1's in bin string) to k_rolls
        # L:    max conseq rolls are less than k
        # LE:   max conseq rolls are less than or equal to k
        # G:    min conseq rolls are greater than k
        # GE:   min conseq rolls are greater than or equal to k
        # EQ:   contains conseq rolls equal to k
        # NEQ:  no conseq rolls are equal to k
        def compare_xy(compare_mode,x,y):
            compare_modes = {'LT':'LESS THAN',
                            'LE': 'LESS THAN OR EQUAL',
                            'EQ': 'EQUAL',
                            'NE': 'NOT EQUAL',
                            'GT' : 'GREATER THAN',
                            'GE': 'GREATER THAN OR EQUAL'
                            }
            assert(compare_mode in compare_modes)

            if(compare_mode == 'LT'):
                return (x < y)
            elif(compare_mode == 'LE'):
                return (x <= y)
            elif(compare_mode == 'EQ'):
                return (x == y)
            elif(compare_mode == 'NE'):
                return (x != y)
            elif(compare_mode == 'GT'):
                return (x > y)
            elif(compare_mode == 'GE'):
                return (x >= y)
            return False
        
        N = len(input_bin_str)
        ii=0; conseq_rolls=0; max_conseq_rolls = 0
        while(ii<N):
            if(input_bin_str[-ii-1] == '1'):
                conseq_rolls+=1
                max_conseq_rolls = max(max_conseq_rolls,conseq_rolls)
                if(compare_mode in {'GT','GE'}):
                    if(compare_xy(compare_mode,conseq_rolls,k_rolls)==True):
                        return True
                elif(compare_mode in {'LT','LE'}):
                    if(compare_mode == 'LT' and compare_xy('GE',conseq_rolls,k_rolls)==True):
                        return False
                    elif(compare_mode == 'LE' and compare_xy('GT',conseq_rolls,k_rolls)==True):
                        return False
            else:
                if(compare_mode in {'EQ','NE'}):
                    if(compare_mode == 'EQ' and compare_xy('EQ',conseq_rolls,k_rolls)==True):
                        return True
                conseq_rolls=0
            ii+=1
        # after final bit is checked:
        if(compare_mode in {'EQ','NE'}):
            if(compare_mode == 'EQ' and compare_xy('EQ',conseq_rolls,k_rolls)==True):
                return True
        elif(compare_mode in {'LT','LE'}):
            return(compare_xy(compare_mode,max_conseq_rolls,k_rolls))
        return False

    def calc_permute_chance(input_bin_str, p_chance):
        N = len(input_bin_str)
        ii=0; permute_chance = 1
        while(ii<N):
            if(input_bin_str[-ii-1] == '1'):
                permute_chance *= p_chance
            else:
                permute_chance *= (1-p_chance)
            ii+=1
        return permute_chance
        
    def parse_option(input_form):
        if input_form.calc_method == 'mcm':
            return(mcm(input_form.p_chance, input_form.k_rolls, input_form.N_rolls, input_form.N_mcm))
        elif input_form.calc_method == 'bruteforce':
            return(bruteforce(input_form.p_chance, input_form.k_rolls, input_form.N_rolls))
    
    return(parse_option(input_form))


if __name__ =='__main__':
    input_form = user_input_form.ask_form()
    #input_form = user_input_form('bruteforce',0.05,3,10,0)
    #print('Probability = {x}'.format(x=calculate_seq_chance(input_form)))
    #print()
    #input_form = user_input_form('mcm',0.05,3,30,100000)
    print('Probability = {x}'.format(x=calculate_seq_chance(input_form)))
