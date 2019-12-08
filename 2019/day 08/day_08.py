import numpy as np
from itertools import dropwhile

def txt_to_layers(txt, wide, tall):
    digits = np.array([int(i) for i in txt])
    layers = digits.reshape(-1,tall,wide)
    return layers

with open('input.txt', 'r') as f:
    data_txt = f.read().strip()

layers = txt_to_layers(data_txt, 25, 6)
print(layers.shape)
# layer with fewest zero digits
fewest_zero_layer_idx = np.argmin(np.sum(layers==0, axis=(1,2)))
fewest_zero_layer = layers[fewest_zero_layer_idx]
fewest_zero_layer_values = fewest_zero_layer.ravel()
part1_sol = np.sum(fewest_zero_layer_values == 2) * np.sum(fewest_zero_layer_values == 1)
print('Part 1:', part1_sol)
assert(1703 == part1_sol)

BLACK = 0
WHITE = 1
TRANSPARENT = 2

def decode_layers(layers):
    image = np.zeros((layers.shape[1], layers.shape[2]), dtype=np.uint8)
    for y in range(layers.shape[1]):
        for x in range(layers.shape[2]):
            pixel_layers = layers[:,y,x]
            non_transparent = dropwhile(lambda p : p == TRANSPARENT, pixel_layers)
            color = next(non_transparent)
            image[y,x] = color
    return image

def print_image(image):
    for r in image:
        print(''.join([{'0':' ', '1':'.'}[c] for c in map(str, r)]))

print('Part 2:')
print_image(decode_layers(layers))