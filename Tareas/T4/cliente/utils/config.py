from utils.config import get_config
from cliente.parametros import CLIENT_FOLDER


def get_socket_config():
    return get_config(CLIENT_FOLDER, "conexion-socket.json")


def get_webservice_config():
    return get_config(CLIENT_FOLDER, "conexion-webservice.json")


def get_api_url():
    port, host = get_webservice_config()

    return f"http://{host}:{port}"


def get_font():
    return "Arial"
