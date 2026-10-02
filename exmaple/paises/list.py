import os
raw = os.listdir(".")
nombres = []
for nombre in raw:
    if ".txt" in nombre:
        nombres.append(nombre)
result = "{\n"

for file in nombres:
    with open(file, "r", encoding="utf-8") as raw:
        for nombre in raw.readlines():
            print(nombre)
            nombre_sin_espacio = nombre.replace(" ", "")
            result = result + (f'"{nombre.lower().strip()}":"{nombre_sin_espacio.lower().strip()}",\n')

result = result + "}"
with open("resultado.txt", "w", encoding="utf-8") as textos:
    textos.write(result)