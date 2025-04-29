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
        self.send_to_server(["subscribe", pseudo, role.value])

    def send_action(self):
        pseudo = input("Votre pseudo : ").strip().upper()
        try:
            dx = int(input("Déplacement X (-1, 0, 1) : "))
            dy = int(input("Déplacement Y (-1, 0, 1) : "))
            move = Move(dx, dy)
        except ValueError:
            print("Déplacements invalides. Entrez -1, 0 ou 1.")
            return
        self.send_to_server(["action", pseudo] + move.to_list())

    def quit(self):
        print("Fermeture du client.")
        self.running = False

    def invalid_choice(self):
        print("Choix invalide.")

    def run(self):
        actions = {
            '1': self.subscribe,
            '2': self.send_action,
            '3': self.quit
        }

        while self.running:
            print("\n--- Menu ---")
            print("1. S'inscrire")
            print("2. Envoyer une action")
            print("3. Quitter")
            choice = input("Choix : ")

            # Récupération de la fonction à appeler ou fallback
            actions.get(choice, self.invalid_choice)()


if __name__ == '__main__':
    client = Client()
    client.run()
