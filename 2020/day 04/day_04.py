"""
Advent of Code 2020 - Day 04
Pieter Kitslaar
"""

from pathlib import Path
from functools import reduce

example_passports="""\
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

def parse(input_batch):
    passports = [{}]
    for line in input_batch.splitlines():
        if not line:
            passports.append({})
        else:
            for info in line.split():
                k,v = info.split(':')
                passports[-1][k]=v
    return passports

ALL_KEYS=dict(line.split(' ',1) for line in """\
byr (Birth Year)
iyr (Issue Year)
eyr (Expiration Year)
hgt (Height)
hcl (Hair Color)
ecl (Eye Color)
pid (Passport ID)
cid (Country ID)""".splitlines())

def solve(input_batch, ignore_missing_fields={'cid',}):
    passports = parse(input_batch)
    expected_keys = set(ALL_KEYS) - ignore_missing_fields
    num_valid = len([p for p in passports if len(expected_keys - set(p))==0])
    return num_valid
    
def test_example():
    num_valid = solve(example_passports)
    assert(2 == num_valid)

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read().strip()

def test_part1():
    num_valid = solve(get_input())
    assert(216==num_valid)
    print('Part 1:', num_valid)

####
# Part 2
####

#byr (Birth Year) - four digits; at least 1920 and at most 2002.
def byr(txt):
    return 1290 <= int(txt) <= 2002

#iyr (Issue Year) - four digits; at least 2010 and at most 2020.
def iyr(txt):
    return 2010 <= int(txt) <= 2020

#eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
def eyr(txt):
    return 2020 <= int(txt) <= 2030

#hgt (Height) - a number followed by either cm or in:
#If cm, the number must be at least 150 and at most 193.
#If in, the number must be at least 59 and at most 76.
def hgt(txt):
    height_txt, unit = txt[:-2], txt[-2:]
    height = int(height_txt)
    if unit == 'cm':
        return 150 <= height <= 193
    elif unit == 'in':
        return 59 <= height <= 76
    return False

#hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
def hcl(txt):
    return len(txt)==7 and '#' == txt[0] and all(c in '0123456789abcdef' for c in txt[1:])

#ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
def ecl(txt):
    return txt in ('amb','blu','brn','gry','grn','hzl','oth')

#pid (Passport ID) - a nine-digit number, including leading zeroes.
def pid(txt):
    return len(txt)==9 and all(c.isdigit() for c in txt)

#cid (Country ID) - ignored, missing or not.
def cid(txt):
    return True

FIELD_VALIDATORS = {k:globals()[k] for k in ALL_KEYS}

example_fields ="""\
byr valid:   2002
byr invalid: 2003

hgt valid:   60in
hgt valid:   190cm
hgt invalid: 190in
hgt invalid: 190

hcl valid:   #123abc
hcl invalid: #123abz
hcl invalid: 123abc

ecl valid:   brn
ecl invalid: wat

pid valid:   000000001
pid invalid: 0123456789"""

def test_field_validations():
    for line in example_fields.splitlines():
        if line:
            f_name, is_valid, f_value = line.split()
            f_name = f_name.strip()
            is_valid = not 'invalid' in is_valid
            f_value = f_value.strip()

            validator = FIELD_VALIDATORS[f_name]
            assert(is_valid == validator(f_value))

def validate_passport(p):
    expected_fields = set(FIELD_VALIDATORS) - {'cid',}
    for f in expected_fields:
        try:
            if f not in p or not FIELD_VALIDATORS[f](p[f]):
                return False
        except ValueError:
            return False
    return True

invalid_passports="""\
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""

def test_invalid_passports():
    passports = parse(invalid_passports)
    for p in passports:
        assert(False == validate_passport(p))

valid_passports="""\
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""

def test_valid_passports():
    passports = parse(valid_passports)
    for p in passports:
        assert(True == validate_passport(p))

def solve2(input_batch):
    passports = parse(input_batch)
    num_valid = len([p for p in passports if validate_passport(p)])
    return num_valid

def test_part2():
    num_valid = solve2(get_input())
    assert(150==num_valid)
    print('Part 2:', num_valid)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_field_validations()
    test_invalid_passports()
    test_valid_passports()
    test_part2()
    