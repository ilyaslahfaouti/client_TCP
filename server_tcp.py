import socket
import json

HOST = 'localhost' 
PORT = 9999        r

# Créer la socket du serveur
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
    server_sock.bind((HOST, PORT)) 
    server_sock.listen(1)          
    print("Serveur en écoute sur", HOST, ":", PORT)

    # Accepter une connexion entrante
    conn, addr = server_sock.accept()
    with conn:
        print(f"Connexion établie avec {addr}")

        # Recevoir les données du client
        data = conn.recv(1024)
        if data:
            print("Données reçues:", data.decode('utf-8'))

            # Convertir les données JSON reçues
            json_data = json.loads(data.decode('utf-8'))

            # Exemple de réponse
            if json_data['type'] == 'subscribe':
                response = {
                    'status': 'success',
                    'message': f"Joueur {json_data['pseudo']} inscrit en tant que {json_data['role']}."
                }
            elif json_data['type'] == 'action':
                response = {
                    'status': 'success',
                    'message': f"Joueur {json_data['pseudo']} a effectué un déplacement {json_data['action']}."
                }
            else:
                response = {
                    'status': 'error',
                    'message': 'Type inconnu.'
                }

            # Envoyer une réponse au client
            conn.sendall(json.dumps(response).encode('utf-8'))
