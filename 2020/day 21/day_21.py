
"""
Advent of Code 2020 - Day 21
Pieter Kitslaar
"""

from pathlib import Path

example="""\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""

def parse(txt):
    foods = []
    for line in txt.splitlines():
        ingredients_txt, _, contains_txt = line.partition('(contains')
        ingredients = set([i.strip() for i in ingredients_txt.split()])
        known_allergens = set([a.strip() for a in contains_txt[:-1].split(',')])
        foods.append({'ingredients': ingredients, 'allergens': known_allergens})
    return foods

def solve1(food_list):
    all_ingredients = set([i for f in food_list for i in f['ingredients']])
    all_allergens = set([a for f in food_list for a in f['allergens']])

    # Find all possible options by looping over all 
    # ingredients and assume they contain the allergen
    # if the allergen is mentioned in a food, than
    # it should contain the ingredient
    ingredient_to_allergen_options = {}
    for ing in all_ingredients:
        options = ingredient_to_allergen_options[ing] = {}
        for allergen in all_allergens:
            this_option = options[allergen] = []
            found_mismatch = False

            # assume ing contains allergen
            # so if the allergen is listed, the ingredient should be
            # in the list
            for i, f in enumerate(food_list):
                if allergen in f['allergens'] and ing not in f['ingredients']:
                    found_mismatch = True
                    this_option.clear()
                    break
                else:
                    this_option.append(i)

    # Find ingredients that don't have any allergen option
    non_allergens = set()
    for ing, options in ingredient_to_allergen_options.items():
        if all(len(o)==0 for o in options.values()):
            non_allergens.add(ing)
    
    # compute how often this 'non_allergen' ingredients are mentioned
    num_times = 0
    for f in food_list:
        this_non_allergens = f['ingredients'].intersection(non_allergens)
        num_times += len(this_non_allergens)
    return num_times, non_allergens


def solve2(food_list, non_allergens):
    # remove non_allergens
    for f in food_list:
        f['ingredients'] = f['ingredients'] - non_allergens

    # Keep looping over all ingredient options
    # and keep removing options that are not possible
    # After each search find ingredients with only a single
    # options and store this in the 'known_ingredients'.
    # Next clear the known ingredients and allergens from the
    # food list. Continue until all options have been found.
    known_ingredients = {}
    removed_options = True
    while removed_options:
        removed_options = False
        ingredient_options = {}
        for f in food_list:
            for ing in f['ingredients']:
                ingredient_options.setdefault(ing, set()).update(f['allergens'])

        for ing, options in ingredient_options.items():
            non_options = set()
            for opt in options:
                # assum 
                for f in food_list:
                    if opt in f['allergens'] and ing not in f['ingredients']:
                        #print(ing, "is NOT", opt)  
                        non_options.add(opt)
            for opt in non_options:
                options.remove(opt)

        for ing, opt in ingredient_options.items():
            if len(opt) == 1:
                known_ingredients[ing] = list(opt)[0]
                removed_options = True

        known_ing_names = set(known_ingredients)
        known_allergen_names = set(known_ingredients.values())
        new_food_list = []
        for f in food_list:
            new_ing = f['ingredients'] - known_ing_names
            if new_ing:
                new_allerg = f['allergens'] - known_allergen_names
                new_food_list.append({'ingredients': new_ing, 'allergens': new_allerg})
        food_list = new_food_list
    sorted_ingredients = [t[0] for t in sorted(known_ingredients.items(), key=lambda t: t[1])]
    return ",".join(sorted_ingredients)

def test_example():
    food_list = parse(example)
    answer, non_allergens = solve1(food_list)
    assert(5 == answer)
    answer2 = solve2(food_list, non_allergens)
    assert("mxmxvkd,sqjhc,fvjkl" == answer2)

def get_input(name='input.txt'):
    with open(Path(__file__).parent / name, 'r') as f:
        return f.read()   
    
def test_puzzle():
    food_list = parse(get_input())
    answer, non_allergens = solve1(food_list)
    print('Part 1:', answer)
    assert(1958 == answer)
    answer2 = solve2(food_list, non_allergens)
    print('Part 2:', answer2)
    assert("xxscc,mjmqst,gzxnc,vvqj,trnnvn,gbcjqbm,dllbjr,nckqzsg" == answer2)

if __name__ == "__main__":
    test_example()
    test_puzzle()