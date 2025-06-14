import time


def log(message: str) -> None:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    print(f"[{timestamp}] {message}")
