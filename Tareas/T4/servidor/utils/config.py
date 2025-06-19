from utils.config import get_config
from servidor.parametros import SERVER_FOLDER


def get_socket_config():
    return get_config(SERVER_FOLDER, "conexion-socket.json")


def get_webservice_config():
    return get_config(SERVER_FOLDER, "conexion-webservice.json")


def get_api_url():
    port, host = get_webservice_config()

    return f"http://{host}:{port}"
