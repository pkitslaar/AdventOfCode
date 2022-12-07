"""
Advent of Code 2022 - Day 07
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read()


EXAMPLE_DATA="""\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

def cum_size(file_system, dir_path='/'):
    this_size = 0
    for child in file_system[dir_path]['children']:
        if file_system[child]['type'] == 'dir':
            this_size += cum_size(file_system, child)
        else:
            assert(file_system[child]['type']=='file')
            this_size += file_system[child]['size']
    file_system[dir_path]['cum_size'] = this_size
    return this_size

def parse(d):
    file_system = {'/': {'name': '/', 'type': 'dir', 'size': 0, 'children': []}}
    current_dir = '/'
    for line in d.strip().splitlines():
        if line.startswith('$ cd'):
            cd_arg = line[5:]
            if cd_arg == "/":
                current_dir = "/"
            elif cd_arg == "..":
                current_dir = "/".join(current_dir.split('/')[:-1]) or '/'
            else:
                new_dir = f"{current_dir.rstrip('/')}/{cd_arg}"
                assert(new_dir in file_system[current_dir]['children'])
                current_dir = new_dir
        elif line.startswith('$ ls'):
            # dir listing
            pass
        elif line.startswith('dir'):
            dir_name = line.split()[1]
            full_dir_name = f"{current_dir.rstrip('/')}/{dir_name}" 
            dir_dict = {'name': full_dir_name, 'type': 'dir', 'size': 0, 'children': []}
            file_system[full_dir_name] = dir_dict
            file_system[current_dir]['children'].append(full_dir_name)
        else:
            f_size = int(line.split()[0])
            f_name = line.split()[1]
            full_path = f"{current_dir.rstrip('/')}/{f_name}"
            file_dict = {'name': full_path, 'type': 'file', 'size': f_size, 'children': []}
            file_system[full_path] = file_dict
            file_system[current_dir]['children'].append(full_path)
    cum_size(file_system)
    return file_system

def test_parse():
    fs = parse(EXAMPLE_DATA)
    assert(584 == fs['/a/e']['cum_size'])
    assert(94853 == fs['/a']['cum_size'])
    assert(24933642 == fs['/d']['cum_size'])
    assert(48381165 == fs['/']['cum_size'])

def solve(d):
    fs = parse(d)
    total_sum = sum(info['cum_size'] for d,info in fs.items() if info['type']=='dir' and info['cum_size'] <= 100000)
    return total_sum

def test_example():
    assert(95437 == solve(EXAMPLE_DATA))

def test_part1():
    result = solve(data())
    print('PART 1:', result)

def solve2(d):
    fs = parse(d)
    DISK_SIZE = 70000000
    NEEDED_SPACE = 30000000

    current_space = DISK_SIZE - fs['/']['cum_size']
    space_to_free = NEEDED_SPACE - current_space
    assert(space_to_free >= 0)

    space_to_dir = []
    for d, info in fs.items():
        if info['type'] == 'dir' and info['cum_size']>=space_to_free:
            space_to_dir.append((info['cum_size'], d))
    space_to_dir.sort()
    print(space_to_dir[0])
    return space_to_dir[0][0]

def test_example2():
    result = solve2(EXAMPLE_DATA)
    assert(24933642 == result)

def test_part2():
    result = solve2(data())
    print('PART 2:', result)

if __name__ == "__main__":
    test_parse()
    test_example()
    test_part1()
    test_example2()
    test_part2()

