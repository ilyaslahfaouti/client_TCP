import socket
import json
from enum import Enum

class Role(Enum):
    WOLF = "wolf"
    VILLAGER = "villager"

    @staticmethod
    def from_input(input_str):
        input_str = input_str.strip().lower()
        if input_str == "wolf":
            return Role.WOLF
        elif input_str == "villager":
            return Role.VILLAGER
        else:
            return None

class Move:
    def __init__(self, dx: int, dy: int):
        if dx not in [-1, 0, 1] or dy not in [-1, 0, 1]:
            raise ValueError("dx and dy must be -1, 0, or 1.")
        self.dx = dx
        self.dy = dy

    def to_list(self):
        return [self.dx, self.dy]

class Client:
    HOST = 'localhost'
    PORT = 9999

    def __init__(self):
        self.running = True

    def send_to_server(self, data):
        message = json.dumps(data)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((self.HOST, self.PORT))
                sock.sendall(message.encode('utf-8'))
                response = sock.recv(4096)
                print("Réponse du serveur :", response.decode('utf-8'))
            except ConnectionRefusedError:
                print("Erreur : impossible de se connecter au serveur.")

    def subscribe(self):
        pseudo = input("Pseudo (1 lettre) : ").strip().upper()
        role_input = input("Rôle (wolf/villager) : ")
        role = Role.from_input(role_input)
        if not role:
            print("Rôle invalide. Choisissez 'wolf' ou 'villager'.")
            return
        data = {
            "subscribe": {
                "pseudo": pseudo,
                "role": role.value
            }
        }
        self.send_to_server(data)

    def send_action(self):
        pseudo = input("Votre pseudo : ").strip().upper()
        try:
            dx = int(input("Déplacement X (-1, 0, 1) : "))
            dy = int(input("Déplacement Y (-1, 0, 1) : "))
            move = Move(dx, dy)
        except ValueError:
            print("Déplacements invalides. Entrez -1, 0 ou 1.")
            return
        data = {
            "action": {
                "pseudo": pseudo,
                "move": move.to_list()
            }
        }
        self.send_to_server(data)

    def list_games(self):
        data = {
            "list_games": {}
        }
        self.send_to_server(data)

    def run(self):
        while self.running:
            print("\n--- Menu ---")
            print("1. S'inscrire")
            print("2. Envoyer une action")
            print("3. Liste des parties en attente")
            print("4. Quitter")
            choice = input("Choix : ")

            if choice == '1':
                self.subscribe()
            elif choice == '2':
                self.send_action()
            elif choice == '3':
                self.list_games()
            elif choice == '4':
                print("Fermeture du client.")
                self.running = False
            else:
                print("Choix invalide.")


if __name__ == '__main__':
    client = Client()
    client.run()
