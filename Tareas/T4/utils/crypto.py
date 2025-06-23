from parametros import CLAVE_CIFRADO


def xor_cipher(data: bytes) -> bytes:
    """
    Code extracted doing modifications from my "XOR Encryption Algorithm"; that is, a function by
    101computing, retrieved on June 13, 2025, from
    https://www.101computing.net/xor-encryption-algorithm/
    """

    values = []

    for i, byte in enumerate(data):
        key = ord(CLAVE_CIFRADO[i % len(CLAVE_CIFRADO)])
        values.append(byte ^ key)

    return bytes(values)
