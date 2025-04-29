import socket
import json

# Fonction pour envoyer les données JSON au serveur TCP
def send_json_to_server(json_data):
    HOST = 'localhost'  # Adresse du serveur
    PORT = 9999         # Port du serveur

    # Convertir les données en JSON
    message = json.dumps(json_data)

    # Création de la socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))  # Se connecter au serveur
        sock.sendall(message.encode('utf-8'))  # Envoyer les données au serveur

        # Recevoir la réponse du serveur
        response = sock.recv(1024)
        print("Réponse du serveur:", response.decode('utf-8'))

# Menu interactif pour envoyer des actions
while True:
    print("\n--- Menu ---")
    print("1. S'inscrire")
    print("2. Envoyer une action")
    print("3. Quitter")
    choice = input("Choix : ")

    if choice == '1':
        pseudo = input("Pseudo (1 lettre) : ").upper()
        role = input("Rôle (wolf/villager) : ").lower()
        send_json_to_server({
            'type': 'subscribe',
            'pseudo': pseudo,
            'role': role
        })

    elif choice == '2':
        pseudo = input("Votre pseudo : ").upper()
        dx = int(input("Déplacement X (-1, 0, 1) : "))
        dy = int(input("Déplacement Y (-1, 0, 1) : "))
        send_json_to_server({
            'type': 'action',
            'pseudo': pseudo,
            'action': [dx, dy]
        })

    elif choice == '3':
        break
    else:
        print("Choix invalide.")
