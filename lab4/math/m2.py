def Trapezoid(a, b, h):
    area = (a+b)/2*h
    return area

a = int(input("Base, first value: "))
b = int(input("Base, second value: "))
h = int(input("Height: "))

print(Trapezoid(a, b, h))