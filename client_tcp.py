import socket
import json


def send_list_to_server(lst_data):
    HOST = 'localhost'
    PORT = 9999
    message = json.dumps(lst_data)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((HOST, PORT))  
            sock.sendall(message.encode('utf-8'))  
            response = sock.recv(4096)  
            print("Réponse du serveur :", response.decode('utf-8'))
        except ConnectionRefusedError:
            print("Erreur : impossible de se connecter au serveur.")

def main():
    while True:
        print("\n--- Menu ---")
        print("1. S'inscrire")
        print("2. Envoyer une action")
        print("3. Quitter")
        choice = input("Choix : ")

        if choice == '1':
            pseudo = input("Pseudo (1 lettre) : ").strip().upper()
            role = input("Rôle (wolf/villager) : ").strip().lower()
            if role not in ["wolf", "villager"]:
                print("Rôle invalide. Choisissez 'wolf' ou 'villager'.")
                continue
            send_list_to_server(["subscribe", pseudo, role])

        elif choice == '2':
            pseudo = input("Votre pseudo : ").strip().upper()
            try:
                dx = int(input("Déplacement X (-1, 0, 1) : "))
                dy = int(input("Déplacement Y (-1, 0, 1) : "))
                if dx not in [-1, 0, 1] or dy not in [-1, 0, 1]:
                    raise ValueError
            except ValueError:
                print("Déplacements invalides. Entrez -1, 0 ou 1.")
                continue
            send_list_to_server(["action", pseudo, dx, dy])

        elif choice == '3':
            print("Fermeture du client.")
            break

        else:
            print("Choix invalide.")

if __name__ == '__main__':
    main()
