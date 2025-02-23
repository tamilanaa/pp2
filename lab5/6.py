import re

text = "Hello My name, is. tamilnaak, but you can call me tamiolana"
replacedText = re.sub(r'[ ,.]', ':', text)
print(replacedText)