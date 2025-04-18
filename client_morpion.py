import socket
import threading

IP = "127.0.0.1" #Definition de l'ip du serveur
PORT = 5005 #Definition du port
BUFFERSIZE = 4096 #Definition du buffersize
BALISE_NEW_NAME = "__new_name__:" #Definition de la balise new name reliée à l'evenement qui représente la connexion d'un nouveau joueur
BALISE_MESSAGE = "__message__:" #Definition de la balise message servant à differencier au sein du serveur le type de message (nouveau nom ou tentative) entrée par le joueur
S = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # definition de l'interface réseau
name = input("Entrez votre nom : ") 
message_first_conn = BALISE_NEW_NAME + name #Message envoyé au serveur qui lui sera utile pour savoir qu'il faut utiliser la fonction "enregistre joueur"
S.sendto(message_first_conn.encode(), (IP,PORT)) #Envoie du message de première connexion


def send():
    """_summary_ 
    Fonction chargée d'envoyer les tentatives entrée par le client, au serveur
    """
    while True: 
        entrée_client = input("")
        Message = BALISE_MESSAGE + entrée_client
        S.sendto(Message.encode(), (IP, PORT)) 
        

def receive():
    """_summary_
    Fonction chargée d'afficher en continue les données envoyées par le serveur
    """
    while True:
        data, addr = S.recvfrom(BUFFERSIZE)
        data = data.decode()
        print(data)


# Creation des processus
send_thread = threading.Thread(target=send) 
recv_thread = threading.Thread(target=receive)
# Lancement des processus
send_thread.start() 
recv_thread.start()