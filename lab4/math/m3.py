"""
Area of regular polygon: A=(n * a^2)/(4 * tan(pi/4)) 
n - number of sides
a - length of a side
"""
from math import *

def Polygon(n, a):
    return floor((n * (a ** 2))/(4 * tan(pi / 4)))

n = int(input("Input number of sides: "))  
a = int(input("Input the length of a side: "))

print("The area of the polygon is: ", Polygon(n, a))