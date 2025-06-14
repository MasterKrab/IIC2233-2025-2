import json
from pathlib import Path
from servidor.server import Server

def main():
    with Path("servidor", "conexion.json").open(encoding="utf-8") as file:
        data = json.load(file)
        port = data["puerto"]
        host = data["host"]
        
    server = Server(port, host)
    
    server.run()
    
    
    
if __name__ == "__main__":
    main()
    