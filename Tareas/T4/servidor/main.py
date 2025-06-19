from threading import Thread

from servidor.server import Server
from servidor.webservice.main import init_webservice
from servidor.utils.config import get_socket_config, get_webservice_config


def run_sockets():
    port, host = get_socket_config()


    server = Server(port, host)

    server.run()


def run_webservice():
    port, host = get_webservice_config()

    init_webservice(port, host)


def main():
    webservice_thread = Thread(target=run_webservice)
    webservice_thread.start()

    sockets_thread = Thread(target=run_sockets)
    sockets_thread.start()


if __name__ == "__main__":
    main()
