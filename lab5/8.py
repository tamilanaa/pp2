import re

text = "MyNameIsTamoilana"

words = re.findall(r'[A-Z][^A-Z]*', text)
print(words)