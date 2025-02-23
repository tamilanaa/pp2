def C2S(CamelCase):
    snake_case = ""
    for char in CamelCase:
        if(char.isupper()):
            snake_case += '_' + char.lower()
        else:
            snake_case += char
    if snake_case.startswith('_'):
        snake_case = snake_case[1:]
    return snake_case

CamelCase = "AppleBananaCherry"

print(C2S(CamelCase))