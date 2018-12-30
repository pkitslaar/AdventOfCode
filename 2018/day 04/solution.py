# Advent of code - 2018
# Day 4
#
# Pieter Kitslaar
#

from datetime import datetime
from collections import Counter, defaultdict

# parse the file and get the events in correct order
events = []
with open('input.txt', 'r') as f:
    for line in f:
        splitted = line.split(']')
        timestamp_txt = splitted[0][1:]
        timestamp = datetime.strptime(timestamp_txt, 
            '%Y-%m-%d %H:%M')
        events.append((timestamp, splitted[1].strip()))
events.sort(key = lambda t: t[0])


# fill calendar with info when guard starts, sleeps and wakes
calendar = {} 
AWAKE, SLEEPS = range(2)
last_guard_info = {}  
for timestamp, what in events:
    day = timestamp.date()
    if what.startswith('Guard #'):
        guard_id = what.split('#',1)[1].split()[0]
        last_guard_info = {
            'id': guard_id, 
            'sleeps': [], 
            'last_status': AWAKE}

    else:
        if not day in calendar:
            calendar[day] = last_guard_info
        last_status = last_guard_info['last_status']
        if what == 'wakes up':
            assert(SLEEPS == last_status)
            last_guard_info['last_status'] = AWAKE
            last_guard_info['sleeps'][-1]['end'] = timestamp.minute
        elif what == 'falls asleep':
            assert(AWAKE == last_status)
            last_guard_info['last_status'] = SLEEPS
            last_guard_info['sleeps'].append({
                'start': timestamp.minute,
                'end': None,})
        else:
            raise ValueError(f'Unknown status {what}')

# expand the start and end times as explicit
# entries in minute table (e.g. 60 1-minute slots)
total_sleeps_per_guard = Counter()
for d, info in calendar.items():
    # create minute table
    minute_status = [AWAKE]*60 # fill empty (e.g. awake)
    for sleep in info['sleeps']:
        for m in range(sleep['start'], sleep['end']):
            minute_status[m] = SLEEPS
    info['minute_status'] = minute_status

    # get total minutes of sleep
    minutes_sleeping = sum(minute_status)
    info['total_minutes_sleeping'] = minutes_sleeping

    # sum the total minutes of sleep per guard
    total_sleeps_per_guard.update({info['id']: minutes_sleeping})

def get_shifts(guard_id):
    """Filter calendar for particular guard"""
    return [i for i in calendar.items() if i[1]['id'] == guard_id]

def print_shifts_table(shifts_of_guard):
    """Print nice table showing the sleeping times for a set of shifts."""
    print(' '*10, ''.join(str(i//10) for i in range(60)))
    print(' '*10, ''.join(str(i%10) for i in range(60)))
    for d, info in shifts_of_guard:
        print(d, ''.join('.#'[i] for i in info['minute_status']))

# get the most sleeping
most_sleeping_guard, total_minutes = total_sleeps_per_guard.most_common(1)[0]
print('Most sleeping guard is', most_sleeping_guard, 'with a total of', total_minutes, 'minutes')

shifts_of_guard = get_shifts(most_sleeping_guard)
print('Number of shifts for this guard:', len(shifts_of_guard))

print_shifts_table(shifts_of_guard)

sleep_minute_histogram = Counter()
for d, info in shifts_of_guard:
    sleep_minute_histogram.update({i:v for i,v in enumerate(info['minute_status'])})
most_occuring_minute_of_sleep, number_of_times = sleep_minute_histogram.most_common(1)[0]
print('Most occuring minute of sleep', most_occuring_minute_of_sleep, 'which occured', number_of_times, 'times')

print('PART 1:', int(most_sleeping_guard)*most_occuring_minute_of_sleep)

minute_frequences_per_guard = defaultdict(Counter)
for info in calendar.values():
    guard_counter = minute_frequences_per_guard[info['id']]
    guard_counter.update({i:v for i,v in enumerate(info['minute_status'])})

def sort_by_most_common_value(item):
    k, v = item
    minute, count = v.most_common(1)[0]
    return count

most_frequently_asleep_list = sorted(minute_frequences_per_guard.items(), key = sort_by_most_common_value, reverse=True)
most_frequently_asleep = most_frequently_asleep_list[0]
mfa_guard = most_frequently_asleep[0]
mfa_minute = most_frequently_asleep[1].most_common(1)[0]
print('PART 2: guard', mfa_guard, 'during minute', mfa_minute[0], 'occurend', mfa_minute[1], 'times.')
print_shifts_table(get_shifts(mfa_guard))
print('PART 2 ANSWER:', int(mfa_guard)*mfa_minute[0])

