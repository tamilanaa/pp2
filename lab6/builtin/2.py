s = input()
up, low = 0, 0

for char in s:
    if(char.isupper()):
        up += 1
    else:
        low += 1

print(up, low)