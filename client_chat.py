import socket
import threading

IP = "127.0.0.1"
PORT = 5005
BUFFERSIZE = 4096
BALISE_NEW_NAME = "__new_name__:"
BALISE_MESSAGE = "__message__:" 
BALISE_QUIT="__quit__"
S = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
nom_joueur = input("Enter your name : ")
message_first_conn = BALISE_NEW_NAME + nom_joueur
S.sendto(message_first_conn.encode(), (IP,PORT))

def send():
    while True: 
        entrée_client = input("")
        if entrée_client == "quit":
            Message = BALISE_QUIT + entrée_client
            S.sendto(Message.encode(), (IP,PORT))
            break
        else:
            Message = BALISE_MESSAGE + entrée_client
            S.sendto(Message.encode(), (IP, PORT)) 
        

def receive():
    while True:
        data, addr = S.recvfrom(BUFFERSIZE)
        print(data.decode())
        if data == "quit":
            break


# Creation des processus
send_thread = threading.Thread(target=send) 
recv_thread = threading.Thread(target=receive)
# Lancement des processus
send_thread.start() 
recv_thread.start()
