import socket
import doctest
import os

IP = "127.0.0.1" # Definition de l'adresse IP du serveur
PORT = 5005 #Définition du port 
BUFFERSIZE = 4096
BALISE_NEW_NAME = "__new_name__:"
BALISE_MESSAGE = "__message__:" 
BALISE_QUIT="__quit__"
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Definition du socket udp
s.bind((IP,PORT)) #Associer l'adresse ip définie au port#

adresses = {
    
}

def send_entrance_notification(addr, name):
    if addr not in adresses:
        adresses[addr] = name
        Msg = f"\n***{name}*** vient de rentrer sur le chat !\n"
        for key in adresses.keys():
            s.sendto(Msg.encode(), key)
    else:
        pass
        

def send_message(addr, message):
    nom_expediteur = adresses[addr]
    Message_envoyé = f"[{nom_expediteur}] : {message}"
    
    for cle in adresses:
        if cle != addr: 
            s.sendto(Message_envoyé.encode(), cle)


def send_quit_notification(addr):
    nom_expediteur = adresses[addr]
    Message_quit = f"\n***{nom_expediteur}*** a quitté le chat.\n"
    for cle in adresses:
        if cle != addr: 
            s.sendto(Message_quit.encode(), cle)

    del adresses[addr]

def traite_data(addr, data):
    data = data.decode()
    
    if data.startswith("__new_name__:"):
        ch = data.split("__new_name__:")
        nom = ch[1]
        send_entrance_notification(addr, nom)
        
    elif data.startswith("__quit__"):
        send_quit_notification(addr)
        end = data.split("__quit__")
        
    elif data.startswith("__message__:"):
        chaine = data.split("__message__:")
        message = chaine[1]
        send_message(addr, message)
        
    
    


while True: 
    Message_entrant, addr = s.recvfrom(BUFFERSIZE)
    mss = Message_entrant.decode()
    if mss.startswith("__quit__"):
        print("recv_data : __quit__")
    else:
        print(f"recv_data : {Message_entrant}")
    traite_data(addr, Message_entrant)


