import socket
import json
from models import Game, Wolf, Villager

HOST = 'localhost'
PORT = 9999

game = Game(nb_max_turn=10, width=10, height=5)
players = {}  # dictionnaire pour stocker les objets Player

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
    server_sock.bind((HOST, PORT))
    server_sock.listen(5)
    print(f"Serveur en écoute sur {HOST}:{PORT}")

    while True:
        conn, addr = server_sock.accept()
        with conn:
            print(f"Connexion de {addr}")
            data = conn.recv(1024)
            if not data:
                continue

            try:
                message = json.loads(data.decode('utf-8'))
                print("Message reçu:", message)

                if not isinstance(message, list) or len(message) < 1:
                    raise ValueError("Format invalide")

                msg_type = message[0]

                if msg_type == "subscribe":
                    _, pseudo, role = message
                    if role == "wolf":
                        player = Wolf(pseudo)
                    elif role == "villager":
                        player = Villager(pseudo)
                    else:
                        raise ValueError("Rôle inconnu")

                    game._Game__gameboard.subscribe_player(player)
                    players[pseudo] = player

                    response = {
                        "status": "success",
                        "message": f"{pseudo} inscrit comme {role}"
                    }

                elif msg_type == "action":
                    _, pseudo, dx, dy = message
                    player = players.get(pseudo)
                    if not player:
                        raise ValueError("Joueur inconnu")

                    game.register_action(player, (dx, dy))
                    game.process_action()
                    game._Game__gameboard.end_round()

                    response = {
                        "status": "success",
                        "message": f"{pseudo} a bougé ({dx},{dy})",
                        "gameboard": str(game._Game__gameboard)
                    }

                else:
                    response = {"status": "error", "message": "Type inconnu"}

            except Exception as e:
                response = {"status": "error", "message": str(e)}

            conn.sendall(json.dumps(response).encode('utf-8'))
