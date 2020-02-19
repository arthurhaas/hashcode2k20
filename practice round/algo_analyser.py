#!/usr/bin/env python
# coding: utf-8

import os

OUTPUT_FOLDER = 'output'

def input(path):
    """Reads in data"""
    
    f = open(path, "r")
    lines = f.readlines()
    f.close()

    [max_slices, num_types] = map(lambda x: int(x), lines[0].rstrip('\n').split(' '))
    pizza_types = list(map(lambda x: int(x), lines[1].rstrip('\n').split(' ')))

    if not (num_types == len(pizza_types)):
        print('Watch out for amout of different types. These are note equal to the first line.')
    
    return [max_slices, num_types, pizza_types]


def solve_1_simple_algo_backwards(max_slices, num_types, pizza_types):
    """Simple iteration from back to front"""
    
    hungry_participants = max_slices
    chosen_pizza_types = []
    
    for i in range(len(pizza_types)-1, -1, -1):
        slices = pizza_types[i]
        if hungry_participants >= slices:
            hungry_participants -= slices
            chosen_pizza_types.append(i)
    
    return sorted(chosen_pizza_types)


def solve_2_simple_algo_forward(max_slices, num_types, pizza_types):
    """Simple iteration from back to front"""
    
    hungry_participants = max_slices
    chosen_pizza_types = []
    
    for i in range(0, len(pizza_types) - 1, 1):
        slices = pizza_types[i]
        if hungry_participants >= slices:
            hungry_participants -= slices
            chosen_pizza_types.append(i)
    
    return sorted(chosen_pizza_types)


def getFalseArray(length):
    falseArray = []
    for i in range(length):
        falseArray.append(False)
    return falseArray


def solve_3_complex_algo_forwards(max_slices, num_types, slices):

    best_array = []
    best_array_slices = []
    used_slices = getFalseArray(len(slices))
    for i in range(len(slices)-1, -1, -1):
        counter = slices[i]
        used_slices[i] = True
        for j in range(len(slices)):
            if used_slices[j] == False:
                if counter + slices[j] <= max_slices:
                    used_slices[j] = True
                    counter += slices[j]
                else:
                    break

        best_array.append(counter)
        used_slices_num = []
        for b in range(len(used_slices)):
            if used_slices[b] == True:
                used_slices_num.append(b)
        best_array_slices.append(used_slices_num)
        used_slices = getFalseArray(len(slices))
        
    maxv = -1
    maxi = -1
    for i in range(len(best_array)):
        if maxv < best_array[i]:
            maxi = i
            maxv = best_array[i]

    return best_array_slices[maxi]


def solve_4_complex_algo_backwards(max_slices, num_types, slices):
    best_array = []
    best_array_slices = []
    used_slices = getFalseArray(len(slices))
    for i in range(len(slices)-1, -1, -1):
        counter = slices[i]
        used_slices[i] = True
        for j in range(i-1, -1, -1):
            if used_slices[j] == False:
                if counter + slices[j] <= max_slices:
                    used_slices[j] = True
                    counter += slices[j]

        best_array.append(counter)
        used_slices_num = []
        for b in range(len(used_slices)):
            if used_slices[b] == True:
                used_slices_num.append(b)
        best_array_slices.append(used_slices_num)
        used_slices = getFalseArray(len(slices))
        
    maxv = -1
    maxi = -1
    for i in range(len(best_array)):
        if maxv < best_array[i]:
            maxi = i
            maxv = best_array[i]
    return best_array_slices[maxi]
    

def output(solution, path):
    """Cleaning and output"""

    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)

    f = open(path, "w")
    f.write(str(len(solution)) + "\n")
    f.write(' '.join(str(pizza_type) for pizza_type in solution))
    f.close()


def calculateScore(solution, pizza_types):
    """Calculating the score"""
    score = 0
    for i in solution:
        score += pizza_types[i]
    return score



if __name__ == '__main__':
    
    paths = ["data/a_example.in",
            "data/b_small.in",
            "data/c_medium.in",
            "data/d_quite_big.in",
            "data/e_also_big.in"]

    for path in paths:
        print("processing file {}".format(path))

        [max_slices, num_types, pizza_types] = input(path)
        scores = {}

        # algo 1
        solution1 = solve_1_simple_algo_backwards(max_slices, num_types, pizza_types)
        score = calculateScore(solution1, pizza_types)
        print("1 - Received a score of {} from possible {}. Leading to missing: {}".format(score, max_slices, max_slices-score))
        
        # algo 2
        solution2 = solve_2_simple_algo_forward(max_slices, num_types, pizza_types)
        score2 = calculateScore(solution2, pizza_types)
        print("2 - Received a score of {} from possible {}. Leading to missing: {}".format(score2, max_slices, max_slices-score2))

        # algo 3
        solution3 = solve_3_complex_algo_forwards(max_slices, num_types, pizza_types)
        score3 = calculateScore(solution3, pizza_types)
        print("3 - Received a score of {} from possible {}. Leading to missing: {}".format(score3, max_slices, max_slices-score3))
        
        # algo 4
        solution4 = solve_4_complex_algo_backwards(max_slices, num_types, pizza_types)
        score4 = calculateScore(solution4, pizza_types)
        print("4 - Received a score of {} from possible {}. Leading to missing: {}".format(score4, max_slices, max_slices-score4))

        #output_path = os.path.join(OUTPUT_FOLDER, path.split('/')[1])
        #output(solution1, output_path)
        print("")
