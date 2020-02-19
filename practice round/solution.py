#!/usr/bin/env python
# coding: utf-8

"""
Google HashCode 2020
Practice Round
"""

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


def getFalseArray(length):
    falseArray = []
    for i in range(length):
        falseArray.append(False)
    return falseArray


def solve(max_slices, num_types, slices):
    """Solving the problem"""

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
        
        solution = solve(max_slices, num_types, pizza_types)
        score = calculateScore(solution, pizza_types)
        print("Received a score of {} from possible {}. Leading to missing: {}".format(score, max_slices, max_slices - score))
        output_path = os.path.join(OUTPUT_FOLDER, path.split('/')[1])
        output(solution, output_path)

        print("")