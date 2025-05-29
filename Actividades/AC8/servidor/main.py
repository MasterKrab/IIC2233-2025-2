import json
import sys

from flask import Flask, request, Response
from wsgiref.simple_server import make_server

from servidor.dcconsumo import DCConsumo


app = Flask(__name__)

dcconsumo = DCConsumo()
dcconsumo.cargar_data()


def generar_respuesta(respuesta: dict, status_code: int) -> Response:
    return Response(
        response=json.dumps(respuesta),
        status=status_code,
        content_type="application/json",
    )


@app.route("/")
def hello_world() -> Response:
    return generar_respuesta({"msg": "Hello World!"}, 200)


@app.route("/obtener_saldo", methods=["GET"])
def obtener_saldo_total() -> Response:
    # TODO: Parte I
    return generar_respuesta({"result": dcconsumo.obtener_saldo()}, 200)


@app.route("/obtener_saldo/<banco>", methods=["GET"])
def obtener_saldo_banco(banco: str) -> Response:
    # TODO: Parte I
    try:
        saldo = dcconsumo.obtener_saldo(banco)
        return generar_respuesta({"result": saldo}, 200)
    except KeyError:
        return generar_respuesta({"error": f"Cuenta {banco} no encontrada"}, 404)


@app.route("/obtener_transacciones/<banco>", methods=["GET"])
def obtener_transacciones(banco: str) -> Response:
    # TODO: Parte I
    try:
        transacciones = dcconsumo.obtener_transacciones(banco, None)
        return generar_respuesta({"result": transacciones}, 200)
    except KeyError:
        return generar_respuesta({"error": f"Cuenta {banco} no encontrada"}, 404)


@app.route("/agregar_gasto/<banco>", methods=["POST"])
def agregar_gasto(banco: str) -> Response:
    titulo = request.args.get("titulo", type=str)
    monto = request.args.get("monto", type=int)

    if titulo is None or monto is None:
        return generar_respuesta({"error": "Faltan argumentos"}, 400)

    try:
        dcconsumo.agregar_gasto(banco, titulo, monto)
    except KeyError:
        return generar_respuesta({"error": f"Cuenta {banco} no encontrada"}, 404)

    return generar_respuesta({"msg": "Gasto agregado"}, 200)


@app.route("/ajustar_saldo/<banco>", methods=["PATCH"])
def ajustar_saldo(banco: str) -> Response:
    saldo = request.args.get("saldo", type=int)

    if saldo is None:
        return generar_respuesta({"error": "Faltan argumentos"}, 400)
    try:
        dcconsumo.ajustar_saldo(banco, saldo)
    except KeyError:
        return generar_respuesta({"error": f"Cuenta {banco} no encontrada"}, 404)

    return generar_respuesta({"msg": "Saldo ajustado"}, 200)


@app.route("/hacer_transferencia", methods=["POST"])
def hacer_transferencia() -> Response:
    token = request.args.get("Authorization", type=str)


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4160 if len(sys.argv) < 2 else int(sys.argv[1])

    with make_server(HOST, PORT, app) as httpd:
        try:
            print(f"Iniciando servidor: http://{HOST}:{PORT}")
            print("""Utiliza 'Ctrl + C' o 'Cmd + C' para apagar el servidor""")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nApagando servidor")
            httpd.shutdown()
