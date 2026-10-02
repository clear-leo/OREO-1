import os, json
jsons = os.listdir(".")
angulos = {"américa": 18, "europa": -90, "asia": -170, "áfrica": -77, "oceanía": -200}
result = {}
for archivo_nombre in jsons:
    if not ".json" in archivo_nombre:
        continue
    with open(archivo_nombre, "r", encoding="utf-8") as archivo:
        data = json.load(archivo)
    for pais in data["paises"]:
        info_top = f'{pais["resumen"]}\n'

        result[pais["nombre"].lower().strip().replace(" ", "")] = {
            "nombre": pais["nombre"].strip(),
            "info_top": info_top,
            "capital": pais["capital"].capitalize(),
            "idioma": pais["idiomas"][0].capitalize(),
            "mejor_epoca": pais["mejor_epoca"],
            "costo": pais["costo"],
            "info_bottom": pais["cultura"] + pais["consejo"],
            "imagen": f'images/{data["continente"]["nombre"].lower().strip()}.png',
            "angulo": angulos[data["continente"]["nombre"].lower().strip()],
        }


os.remove("../data.json")
with open("../data.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(result))


