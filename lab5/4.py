import re

pattern = re.compile(r"[A-Z]{1}[a-z]+")
print(pattern.findall("Au Ag i F Ch H2O "))