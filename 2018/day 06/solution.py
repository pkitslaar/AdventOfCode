# Advent of code - 2018
# Day 6
#
# Pieter Kitslaar
#

from collections import Counter
import string

with open('input.txt', 'r') as f:
    XY = []
    for line in f:
        XY.append(tuple(map(int, line.split(', '))))
X, Y = zip(*XY) # unpack X and Y par

# find bounding box of points
min_X, max_X = min(X), max(X)
min_Y, max_Y = min(Y), max(Y)
print(min_X, max_X, min_Y, max_Y)

search_min_X = min_X - 1
search_max_X = max_X + 1
search_min_Y = min_Y - 1
search_max_Y = max_Y + 1

def distances(x,y):
    """
    returns Manhattan distances for a particular point (x,y)
    to all locations in XY
    """
    d =  Counter({i:abs(x-X_i)+abs(y-Y_i) for i, (X_i, Y_i) in enumerate(XY)})
    return list(reversed(list(d.most_common())))

infinte = set()
closestAreas = Counter()
for y in range(search_min_Y, search_max_Y):
    y_is_at_border = y in (search_min_Y, search_max_Y-1) 
    for x in range(search_min_X, search_max_X):
        x_is_at_border = x in (search_min_X, search_max_X-1)
        d = distances(x,y)
        if d[0][1] != d[1][1]: # not tied distance with other
            location_id, distance = d[0]
            if y_is_at_border or x_is_at_border:
                infinte.add(location_id)
            closestAreas.update({location_id : 1})
largest = [a for a in closestAreas.most_common() if a[0] not in infinte]
print('PART 1:', largest[0])

total_area = 0
for y in range(search_min_Y, search_max_Y):
    y_is_at_border = y in (search_min_Y, search_max_Y-1) 
    for x in range(search_min_X, search_max_X):
        x_is_at_border = x in (search_min_X, search_max_X-1)
        d = distances(x,y)
        total_distance = sum([t[1] for t in d])
        if total_distance < 10000:
            total_area += 1
print('PART 2:', total_area)
            




            

