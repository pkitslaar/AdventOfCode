from pathlib import Path
import datetime

this_dir = Path(__file__).parent

def get_day_creation_times():
    day_dirs = [d for d in this_dir.glob('day *')]
    day_dirs.sort()
    day_creation = {}
    for d in day_dirs:
        day_number = int(d.stem[4:6])
        day_creation[day_number] = datetime.datetime.fromtimestamp(d.stat().st_birthtime)
    return day_creation

def duration_to_timedelta(duration):
    hours, minutes, seconds = map(int, duration.split(':'))
    return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

def parse_stats():
    day_stats = {}
    with open(this_dir / 'personal_stats.txt','r') as f:
        for line in f:
            if line[1:3].strip().isnumeric():
                parts = [p.strip() for p in line.split()]
                day_number = int(parts[0])
                unlock_time = datetime.datetime(2020, 12, day_number, hour=6)
                part1_duration = duration_to_timedelta(parts[1])
                part1_completion_time = unlock_time + part1_duration
                part2_duration = duration_to_timedelta(parts[4])
                part2_completion_time = unlock_time + part2_duration
                #print(day_number, part1_duration, part1_completion_time, part2_duration, part2_completion_time)
                day_stats[day_number] = {'part1': part1_completion_time, 'part2': part2_completion_time}
    return day_stats
        


if __name__ == "__main__":
    day_creation = get_day_creation_times()
    day_stats = parse_stats()
    day_durations = {}
    all_durations = []
    for d, start_time in day_creation.items():
        p1 = day_stats[d]['part1'] - start_time
        p2 = day_stats[d]['part2'] - start_time
        day_durations[d] = {'part1': p1, 'part2': p2}
        all_durations.extend([p1,p2])
    max_duration = max(all_durations)
    #print(max_duration)
    all_durations.sort()
    median_duartion = all_durations[len(all_durations)//2]
    #print(median_duartion)
    print('Advent of Code 2020 durations - median', median_duartion, 'max', max_duration)
    print(f'day part  h  m |minutes', ' '*51, '|hours')

    for d, durations in day_durations.items():
        for part_num, part_dur in enumerate([durations['part1'], durations['part2'] - durations['part1']]):
            num_minutes = part_dur.seconds//60
            num_hours = num_minutes // 60
            num_minutes -= num_hours*60
            symbol = '.#'[part_num]
            minutes_bar = symbol*(num_minutes if num_hours == 0 else 60)
            hours_bar = symbol*num_hours
            print(f'{" " if part_num else d: >3} {part_num+1: >4} {num_hours:02}:{num_minutes:02} |{minutes_bar: <60}|{hours_bar: <20}')
