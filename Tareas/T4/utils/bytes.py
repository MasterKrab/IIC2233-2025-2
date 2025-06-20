from socket import socket
from math import ceil
from random import shuffle
from utils.crypto import xor_cipher
from parametros import CHUNK_SIZE
import json


def receive_bytes(socket: socket, chunk_size: int, amount: int) -> bytes:
    data = bytes()

    while len(data) < amount:
        remaing = amount - len(data)

        size = min(chunk_size, remaing)

        answer = socket.recv(chunk_size)[:size]

        if len(answer) < size:
            # TODO: Handle this case
            pass

        data += answer

    return data


def divide_in_chunks(data: bytes, chunk_size: int) -> list[bytes]:
    chunks = [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]

    remaing = (
        len(data) % chunk_size if len(data) >= chunk_size else chunk_size - len(data)
    )

    if remaing > 0:
        chunks[-1] += b"\x00" * remaing

    shuffle(chunks)

    return chunks


def receive_message(socket: socket, size: int) -> dict:
    chunks_amount = ceil(size / (CHUNK_SIZE - 4))

    chunks = []

    remaing = size + 4 * chunks_amount

    for i in range(chunks_amount):
        current = min(remaing, CHUNK_SIZE)
        chunk = xor_cipher(receive_bytes(socket, CHUNK_SIZE, current))
        remaing -= current

        number = int.from_bytes(chunk[:4])

        data = chunk[4:]

        chunks.append((number, data))

    chunks.sort(key=lambda chunk: chunk[0])

    message_bytes = b"".join(chunks[1] for chunks in chunks)
    message = json.loads(message_bytes.decode("UTF-8"))

    return message


def create_chunks(message: dict) -> tuple[bytes, list[tuple[int, bytes]]]:
    message_bytes = json.dumps(message).encode("UTF-8")
    message_size = xor_cipher(len(message_bytes).to_bytes(4, "little"))

    chunks = [
        (i, xor_cipher(b"".join([i.to_bytes(4, "little"), chunk])))
        for i, chunk in enumerate(divide_in_chunks(message_bytes, CHUNK_SIZE - 4))
    ]

    return message_size, chunks
