import requests
from cliente.utils.config import get_api_url


def get_game_sets():
    response = requests.get(f"{get_api_url()}/conjuntos")

    if response.status_code != 200:
        return []

    data = response.json()

    return data
