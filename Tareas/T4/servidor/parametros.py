from pathlib import Path

SETS_FOLDER = Path("servidor", "dcconjuntos")

DATABASE_FOLDER = Path("servidor", "database")

USERS_FILE = Path(DATABASE_FOLDER, "usuarios.csv")

GAMES_FILE = Path(DATABASE_FOLDER, "partidas.csv")

USERS_GAMES_FILE = Path(DATABASE_FOLDER, "partidas_usuarios.json")

SERVER_FOLDER = Path("servidor")
