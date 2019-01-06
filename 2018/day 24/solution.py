import re
from collections import namedtuple, Counter

Group = namedtuple('Group', "id army group_id power units hp attack initiative attack_type immune weakness")


example_data = """\
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
"""

IMMUNE, INFECTION = 'Immune System', 'Infection'

def parse(data):
    regex_groups = "units hp immune_weakness attack attack_type initiative".split()
    group_regexp = re.compile('(\d+) units each with (\d+) hit points(.*) with an attack that does (\d+) (.+) damage at initiative (\d+)')
    current_army = None

    empty_group = Group._make([None]*11)

    groups_per_army = Counter()
    groups = []
    for l in  data.splitlines():
        ls = l.strip()
        if not ls:
            continue
        elif ls.endswith(':'):
            current_army = l.split(':')[0]
            continue
        else:
            m = group_regexp.match(ls)
            if not m:
                print(ls)
                raise ValueError()
            group_info = dict(zip(regex_groups, m.groups()))
            group_info['army'] = current_army
            groups_per_army[current_army] += 1
            group_info['immune']=None
            group_info['weakness']=None
            immune_weakness = group_info['immune_weakness']
            if immune_weakness:
                parts = immune_weakness.strip()[1:-1].partition('; ')
                for p in parts[0], parts[2]:
                    for iw_type, info_key in [('immune', 'immune'), ('weak', 'weakness')]:
                        prefix =  f'{iw_type} to '
                        if p.startswith(prefix):
                            attributes = p[len(prefix):].split(', ')
                            group_info[info_key] = tuple(attributes)
            del group_info['immune_weakness']
            for k in 'units hp attack initiative'.split():
                try:
                    group_info[k] = int(group_info[k])
                except ValueError:
                    print(k, group_info)
            group_info['power'] = 0
            group_info['id'] = len(groups)
            group_info['group_id'] = groups_per_army[current_army] 
            #group = empty_group._replace(**group_info)
            groups.append(group_info)
    return groups

class Battle(object):
    def __init__(self, groups, boost = None):
        self.verbose = False
        self.groups = {g['id']:g.copy() for g in groups}
        if boost is not None:
            for g in self.groups.values():
                if g['army'] == IMMUNE:
                    g['attack'] += boost

        self.update_effective_power()

    def _target_select_sort(self, item):
        g = item[1]
        return (-g['power'], -g['initiative'])
    
    def update_effective_power(self):
        for g in self.groups.values():
            g['power'] = g['units']*g['attack']

    def get_army(self, which_army):
        return {v['id']:v for v in self.groups.values() if v['army'] == which_army}

    def get_armies(self):
        armies = {}
        for army in (IMMUNE, INFECTION):
            armies[army] = self.get_army(army)
        return armies

    def damage(self, attacker, defender):
        damage = attacker['units']*attacker['attack']
        if defender['immune'] and attacker['attack_type'] in defender['immune']:
            damage = 0
        elif defender['weakness'] and attacker['attack_type'] in defender['weakness']:
            damage *= 2
        return damage
                    

    def target_selection(self):
        armies = self.get_armies()

        order = list(self.groups.items())
        order.sort(key = self._target_select_sort)

        attack_pairs = []
        for k, g in order:
            target_army = armies[{IMMUNE: INFECTION, INFECTION:IMMUNE}[g['army']]]
            if not target_army:
                continue

            enemy_order = []
            for enemy_group in target_army.values():
                damage = self.damage(g, enemy_group)
                enemy_order.append((damage, enemy_group['power'], enemy_group['initiative'], enemy_group))

            enemy_order.sort()
            best_damage, _, _, best_enemy = enemy_order[-1]
            if best_damage > 0:
                attack_pairs.append((g, best_enemy, damage))
                del target_army[best_enemy['id']]

        if self.verbose:
            for army_type in (IMMUNE, INFECTION):
                print(army_type)
                army = self.get_army(army_type)
                if not army and self.verbose:
                    print('No groups remain')
                for g in army.values():
                    print(f'Group {g["group_id"]} contains {g["units"]} units')
            print()
            for attacker, defender, damage in attack_pairs:
                print(f'{attacker["army"]} group {attacker["group_id"]} would deal defending group {defender["group_id"]} {damage} damage')
            print()
        return attack_pairs

    def attack(self, attack_pairs):
        num_killed_per_army = Counter()
        for attacker, defender, damage in sorted(attack_pairs, key = lambda t: t[0]['initiative'], reverse=True):
            if attacker['units'] > 0:
                damage = self.damage(attacker, defender)
                num_killed = min([damage // defender['hp'], defender['units']])
                num_killed_per_army[defender['army']] += num_killed
                if self.verbose:
                    print(f'{attacker["army"]} group {attacker["group_id"]} attacks defending group {defender["group_id"]}, killing {num_killed} units')
                defender['units'] -= num_killed
        for g in list(self.groups.values()):
            if g['units'] < 1:
                del self.groups[g['id']]
        return sum(num_killed_per_army.values())
        

    def round(self):
        self.update_effective_power()
        attack_pairs = self.target_selection()
        num_killed = self.attack(attack_pairs)
        return num_killed

    def fight(self):
        while True:
            num_attack = self.round()
            if num_attack == 0:
                remaining_units = Counter()
                for g in self.groups.values():
                    remaining_units[g['army']] += g['units']
                remaining_armies = list(remaining_units.keys())
                if len(remaining_armies) == 1:
                    winning_army = remaining_armies[0]
                else:
                    print(remaining_units)
                    winning_army = None # tie
                remaining_units = sum(remaining_units.values())
                if self.verbose:
                    print(self.groups)
                return remaining_units, winning_army

def powerup_immune(d, last_column = None):
    """Perform binary search to find optimal attack boost for Immune (taken from day 15)."""
    lower, upper = [0, 1000] 
    results = {
        lower: (0, None),
        upper: (1, None),
    }
    iteration = 0
    while upper-lower > 1:
        iteration += 1
        mid_point = (lower + upper)//2

        b = Battle(puzzle_data, boost=mid_point)
        #b.verbose = True
        units_left, winning_army = b.fight()
        print(iteration, mid_point, winning_army, units_left)

        success = 1 if winning_army == IMMUNE else 0
        results[mid_point] = (success, (units_left, winning_army))
        if success == 0:
            lower = mid_point
        else:
            upper = mid_point
    print('Took', iteration, 'iterations. Boost is', upper)
    return results[upper][-1]
        
example_groups = parse(example_data)
b = Battle(example_groups)
assert(5216 == b.fight()[0])

b1 = Battle(example_groups, boost=1570)
assert(51 == b1.fight()[0])

with open('input.txt') as f:
    puzzle_data = parse(f.read())
b2 = Battle(puzzle_data)
part1_result = b2.fight()
print(f'PART 1: winning army is {part1_result[1]} with {part1_result[0]} units')

#b_try = Battle(puzzle_data, boost=60)
#b_try.verbose = True
#b_try.fight()

part2_result = powerup_immune(puzzle_data)
print(f'PART 2: winning_army is {part2_result[1]} with {part2_result[0]} units left.')

            
        
        
            
