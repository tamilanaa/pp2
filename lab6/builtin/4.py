'''
Sample Input:
25100
2123
Sample Output:
Square root of 25100 after 2123 miliseconds is 158.42979517754858
'''

import time
import math

def my(num, miliseconds):
    time.sleep(miliseconds / 1000) 

    result = math.sqrt(num)
    return result

num = int(input())
miliseconds = int(input())

output = my(num, miliseconds)
print(f"Square root of {num} after {miliseconds} miliseconds is", output)
