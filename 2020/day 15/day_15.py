"""
Advent of Code 2020 - Day 15
Pieter Kitslaar
"""

def memory_game(txt, N=2020):
    numbers = list(map(int,txt.split(',')))
    history = {number:[i] for i,number in enumerate(numbers)}
    turn = len(numbers)
    last_spoken = numbers[-1]
    while turn < N:
        when_spoken = history[last_spoken]
        speak = 0 # assume first time
        if len(when_spoken) > 1:
            # not first time
            last_two_times = when_spoken[-2:]
            speak = last_two_times[1] - last_two_times[0]
        speak_history = history.setdefault(speak, [])
        history[speak] = speak_history[-1:] + [turn]
        last_spoken = speak
        turn+=1
    return last_spoken

def test_example():
    assert(436 == memory_game("0,3,6"))
    assert(1 == memory_game("1,3,2"))
    assert(10 == memory_game("2,1,3"))
    assert(27 == memory_game("1,2,3"))
    assert(78 == memory_game("2,3,1"))
    assert(438 == memory_game("3,2,1"))
    assert(1836 == memory_game("3,1,2"))

def test_part1():
    answer = memory_game("1,20,11,6,12,0")
    print('Part 1:', answer)
    assert(1085 == answer)

# we don't name it test_part2 since this takes a long time
# to compute and we don't want it to be part of the
# unit tests
def part2():
    answer = memory_game("1,20,11,6,12,0", 30000000)
    print('Part 2:', answer)
    assert(10652 == answer)

if __name__ == "__main__":
    test_example()
    test_part1()
    part2()