'''This program calculates the surface of equilateral 
triangles with sides given on the command line.'''

import sys

def print_triangle_area(side):
    '''calculates the surface of a triangle'''
    area =  round(0.5 * side**2, 2)
    # now print the stuff
    print(f'The area of an equilateral triangle with side {side} is {area}')

for arg in sys.argv[1:]:
    side = float(arg)
    print_triangle_area(side)

