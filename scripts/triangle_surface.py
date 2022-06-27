'''This program calculates the surface of equilateral 
triangles with sides given on the command line.'''

import sys

def print_triangle_area(side):
    area =  0.5 * side**2
    print(f'The area of an equilateral triangle with side \
        {side} is {round(area, 2)}')

for arg in sys.argv[1:]:
    side = float(arg)
    print_triangle_area(side)

