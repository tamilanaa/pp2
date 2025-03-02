import os

f = open("/Users/tamilana/Desktop/PP2/pp22/lab6/dir n files/t4.txt")
cnt = 0
for lines in f:
    cnt += 1
print(f"file has {cnt} lines")