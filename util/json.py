import json


def carregar_json(arquivo_json: str) -> list[dict]:
    with open(arquivo_json, "r", encoding="utf-8") as file:
        dados = json.load(file)
        return dados