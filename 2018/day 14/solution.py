# Advent of code - 2018
# Day 14
#
# Pieter Kitslaar
#

import re

def print_status(data):
    recipes = data['recipes']
    current = data['current']
    text = [f' {s} ' for s in recipes]
    text[current[0]] = f'({recipes[current[0]]})'
    text[current[1]] = f'[{recipes[current[1]]}]'
    print(''.join(text))
    
def next(data):
    recipes = data['recipes']
    #next_recipes = recipes#[:] # copy
    
    current = data['current']
    #next_current = current#[:] # copy
    
    summed = str(recipes[current[0]] + recipes[current[1]])    
    recipes.extend([int(s) for s in summed])
    
    current[0] = (current[0] + recipes[current[0]] + 1) % len(recipes)
    current[1] = (current[1] + recipes[current[1]] + 1) % len(recipes)
    
    return {'recipes': recipes, 'current': current}

def scores_of_ten(after_length, verbose = False):
    data = {
        'recipes': [3, 7],
        'current': [0, 1]
    }
    if verbose:
        print_status(data)
    while True:    
        next(data)
        if verbose:
            print_status(data)
        if len(data['recipes']) - after_length >= 10:
            return ''.join(map(str, data['recipes'][after_length:after_length+10]))
            
def recipes_to_left(pattern_txt, verbose = False):    
    pattern_int = [int(p) for p in pattern_txt]
    data = {
        'recipes': [3, 7],
        'current': [0, 1]
    }
    if verbose:
        print_status(data)
    pattern_length = len(pattern_int)
    final_offset = 0
    while True:
        if  data['recipes'][-pattern_length:] == pattern_int:
            break
        if  data['recipes'][-pattern_length-1:-1] == pattern_int:
            final_offset = 1
            break
        next(data)
        if verbose:
            print_status(data)
    return len(data['recipes']) - pattern_length - final_offset

assert('5158916779' == scores_of_ten(9))
assert('9251071085' == scores_of_ten(18))
assert('5941429882' == scores_of_ten(2018))

assignment_input = '030121'
print(f'PART 1: score for {assignment_input}', scores_of_ten(int(assignment_input)))

assert(9 ==    recipes_to_left('51589'))
assert(5 ==    recipes_to_left('01245'))
assert(18 ==   recipes_to_left('92510'))
assert(2018 == recipes_to_left('59414'))
print(f'PART 2: recipes to left of {assignment_input}', recipes_to_left(assignment_input))
