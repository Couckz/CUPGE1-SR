import socket


IP = "127.0.0.1" # Definition de l'adresse IP du serveur
PORT = 5005 #Définition du port 
BUFFERSIZE = 4096 #Definition du buffersize
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Definition de la liaison entre l'IP et le port
s.bind((IP,PORT)) #Associer l'adresse ip définie au port


#Definition de la grille, étant de dimension invariable quel que soit la partie
grille = [[" 0|", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."], 
          [" 1|", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          [" 2|", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          [" 3|", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."], 
          [" 4|", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          [" 5|", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."], 
          [" 6|", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          [" 7|", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          [" 8|", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          [" 9|", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          ["10|", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          ["11|", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          ["12|", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          ["13|", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          ["14|", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          ["   ------------------------------"],
          ["   ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]]

#Dictionnaire faisant la correspondance entre le tuple addr et le symbole des joueurs
joueur = {
    
}

#Dictionnaire faisant la correspondance entre le tuple addr et le nom des joueurs 
names = {
    
}

#Dictionnaire faisant la correspondance entre le tuple addr et un nombre (0 ou 1), "1" indique que le joueur d'adresse addr est en droit de jouer tandis que "0" indique que le joueur d'adresse addr n'est pas en droit de jouer
tour = {
    
}

#La variable "resultat" contiendra une chaine de caractère représentant la grille
resultat = "" 
for ligne in grille:       
    resultat += " ".join(str(element) for element in ligne) + "\n"   


def enregistre_joueur(addr, name):
    """_summary_
    Fonction ayant pour but d'enregistrer les données des joueurs (adresses, si il est en droit de jouer, nom du joueur),
    dans les différents dictionnaires

    Args:
        addr (_tuple_): _Adresse du joueur enregistré_
        name (_string_): _Nom du joueur que celui-ci a entré_
    """
    
    #Ajout du nom du joueur au dictionnaire names
    names[addr] = name
    
    #Si le symbole "X" n'est pas associé à un joueur, alors le joueur se verra attribuer ce symbole. Dans le cas contraire on lui donnera le symbole "O"
    if "X" not in joueur.values():
        joueur[addr] = "X"
        tour[addr] = 1
        send_message(addr, f"__new_name__:Bienvenue {names[addr]} !")
        
    else:
        joueur[addr] = "O"
        tour[addr] = 0
        send_message(addr, f"__new_name__:Bienvenue {names[addr]} !")
    
    #Boucle qui nous servira à savoir si deux joueurs sont bien connectés pour envoyer la grille à tous les joueurs
    compteur = 0
    for cle in joueur:
        compteur+=1
    
    for adresses in joueur:
        if joueur[adresses] == "X":
            adresse = adresses
    
    #Lorsque les deux joueurs sont bien connectés, on enverra la grille aux joueurs en demandant au joueur courant (possedant le symbole "X") de choisir son prochain coup
    if compteur == 2:
        send_message(addr, f"__COUP__{resultat}")
        send_message(adresse, f"__PCOUP__Entrez votre prochain coup :")
        
         
#La prise en compte de la ligne et de la colonne du coup entré par le joueur est essentiel pour éviter les erreurs de out of range
def check_victoire(grille, symbole, ligne, colonne):
    """_summary_
    Fonction ayant pour but de vérifier à chaque tour si un des joueurs remporte la partie
    
    Args:
        grille (_list_): _Définit la grille de jeu à analyser_
        symbole (_string_): _Définit le symbole du joueur courant_
        ligne (_int_): _Définit la ligne du coup entré par le joueur_
        colonne (_int_): _Définit la colonne du coup entré par le joueur_

    Returns:
        _Bool_: _Si la fonction renvoie True, cela indique que le joueur courant remporte la partie, si ce n'est pas le cas, la fonction renvoie "False"_
        _integer_: _Dans le cas où la grille est pleine, la fonction renvoie le nombre "16" pour indiquer qu'il n'y a plus aucune case libre dans la grille_
    """
          
    counter = 0
    for tab in grille:
        if "." not in tab:
            counter+=1
            
    if counter == 16:
        return counter
    
    ligne = int(ligne)
    
    #Condition de victoire pour un symbole dans une ligne
    compteur = 0
    for j in range(1,15):
        if grille[ligne][j] == symbole:
            compteur+=1

    if compteur == 5:
        return True 
    #Condition cherchant une potentielle victoire pour un symbole dans une colonne
    
    compteur = 0
    for i in range(15):
        if grille[i][colonne] == symbole:
                compteur+=1                             
    
    if compteur == 5:
        return True 
    
    #Condition cherchant une potentielle victoire pour un symbole en diagonale
        #Diagonale y=x
    colonne = int(colonne)
    ligne = int(ligne)
    counter=0
    if grille[ligne][colonne] == symbole:
        counter+=1
        if ligne <= 10 or colonne <= 11:
            for s in range(1,5):
                if grille[ligne-s][colonne+s] == symbole:
                    counter+=1
                if grille[ligne+s][colonne-s] == symbole:
                    counter+=1
                
    
    if counter == 5:
        return True

    #Diagonale y=-x
    counter=0
    if grille[ligne][colonne] == symbole:
        counter+=1
        if ligne <= 10 or colonne <= 11:
            for s in range(1,5):
                if grille[ligne+s][colonne+s] == symbole:
                    counter+=1
                if grille[ligne-s][colonne-s] == symbole:
                    counter+=1
                
    
    if counter == 5:
        return True   
    
    
    return False
     







def mecanique_jeu(addr, message):
        """_summary_ 
            Fonction contrôlant le déoulement du jeu : mise à jour de la grille, verification des coups du joueur courant, s'assure qu'aucun joueur autre que le joueur courant ne peut entrer une tentative, verification d'une potentielle victoire

        Args:
            addr (_tuple_): _adresse du joueur courant_
            message (_string_): _Tentative entrée par le joueur_
        """
    
        #Si un joueur autre que le joueur courant essaie d'entrer une tentative, on lui envoie un message d'erreur
        if tour[addr] != 1:
            send_message(addr, "__NTOUR__Ce n'est pas à vous de jouer !")
            tour[addr] += 1
            
        else:
                        #(Ce code n'est objectivement pas lisible. Celui ci a été programmé ainsi au lieu d'utiliser une boucle for de telle sorte à parer les erreurs de type "timeout du testeur")
                        #Nous cherchons à savoir dans quelle colonne (ABCDE...) va se situer le symbole entré par le joueur
                        colonne = 0
                        if message[0] == "A":
                            colonne +=1
                        if message[0] == "B":
                            colonne +=2
                        if message[0] == "C":
                            colonne +=3
                        if message[0] == "D":
                            colonne +=4
                        if message[0] == "E":
                            colonne +=5
                        if message[0] == "F":
                            colonne +=6
                        if message[0] == "G":
                            colonne +=7
                        if message[0] == "H":
                            colonne +=8
                        if message[0] == "I":
                            colonne +=9
                        if message[0] == "J":
                            colonne +=10
                        if message[0] == "K":
                            colonne +=11
                        if message[0] == "L":
                            colonne +=12
                        if message[0] == "M":
                            colonne +=13
                        if message[0] == "N":
                            colonne +=14
                        if message[0] == "O":
                            colonne +=15

                        #Test servant à connaitre la ligne dans laquelle va se trouver le symbole entré par le joueur. 
                        # Nous différencions le cas où la longueur du message est égale à 2 (exemple tentative "L8") et le cas où la longueur du message est égale à 3 (exemple : B14) de telle sorte à mieux parer les coups invalide (exemple B15)
                        # On étudiera chaque caractère de la chaine entrée par le joueur pour savoir si celle ci correspond bien à un coup valide 
                        if len(message) == 2:
                            ligne = int(message[1])
                        elif len(message) == 3:
                            l = "1" + message[2]
                            ligne = int(l)
                        
                        #Si la longueur du message est égale à 3 et que la ligne du coup indiqué par le joueur est supérieur à 1, le coup est invalide.
                        #En effet pour une "tentative" de longueur 3, son format est [lettre][1, forcément][chiffre]. Dans le cas où le deuxième caractère ne vaut pas 1, on peut déjà dire que le coup est invalide
                        if len(message) == 3 and int(message[1]) > 1:
                            send_message(addr, "__INVALIDE__Coup Invalide !")
                        #Si la tentative contient + de caractère que 3, le coup est considéré comme invalide (au vu des spécifications de la grille)
                        elif len(message) > 3:
                            send_message(addr, "__INVALIDE__Coup Invalide !")
                        #Si la longueur du message est égale à 3 et que la colonne du coup indiqué par le joueur (troisième caractère) est supérieur à 4 (du fait que les lignes ne vont jusqu'à 14), la tentative est considéré comme invalide
                        elif len(message) == 3 and int(message[2]) > 4:
                            send_message(addr, "__INVALIDE__Coup Invalide !")
                        #Si le joueur entre un nom de colonne commençant pas une lettre miniscule, le coup est invalide
                        elif message[0] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                            send_message(addr, "__INVALIDE__Coup Invalide !")
                        #Si le coup entré est (dans la forme) valide, mais que un symbole occupe la position voulue par le joueur, le coup est considéré comme invalide
                        elif grille[ligne][colonne] != ".":
                            send_message(addr, "__INVALIDE__Coup Invalide !")
                            
                        else:
                            
                            #Dans le cas où tous le coup est valide, nous cherchons à savoir si c'est le tour du joueur entrant une tentative. Dans le cas contraire un message d'erreur est envoyé
                            if tour[addr] != 1:
                                send_message(addr, "__NTOUR__Ce n'est pas à vous de jouer !")
                            
                            else:
                                
                                #Boucle servant à reinitialiser les tours à chaque fois qu'un coup valide est entré
                                for key in tour:
                                    tour[key] = 0
                                    tour[addr] = 0 
                                
                                #Boucle servant à indiquer qu'à la prochaine utilisation de la fonction (prochain tour), ce sera au tour du joueur (non courant actuellement) 
                                for key in tour:
                                    if key != addr:
                                        tour[key] = 1  
                             
                                #Condition différenciant le cas où la longueur de la tentative est égale à 3 et le cas où la longueur de la tentative est égale à 2, pour placer le symbole du joueur courant. Cette disjonction est présente pour une meilleure prise en compte de la ligne de la tentative entrée par le joueur
                                if len(message) == 3:
                                    ligne = "1" + str(message[2])
                                    grille[int(ligne)][colonne] = joueur[addr]
                                    
                                else:
                                    grille[int(message[1])][colonne] = joueur[addr]
                                
                                
                                #Boucle servant à transformer la grille en une chaine de caractère
                                resultat = ""
                                for tab in grille:
                                
                                    resultat += " ".join(str(element) for element in tab) + "\n"
                                
                                #Envoie de la nouvelle grille (completée) après que le joueur courant ait placé son symbole
                                send_message(addr, f"__COUP__{resultat}")
                                
                                #Boucle servant à récuperer l'adresse du joueur non courant
                                for cle in joueur:
                                    if cle != addr:
                                        autre_addr = cle
                                
                                #Check de la victoire à chaque tour
                                if check_victoire(grille, joueur[addr], ligne, colonne):
                                    nom = names[addr].split("__new_name__:")
                                    send_message(addr, f"__COUP__{nom[1]} remporte la partie !")
                                    send_message(addr, f"__COUP__Le jeu est terminé ! (Appuyez sur Ctrl+C pour quitter)")
                                elif check_victoire(grille, joueur[addr], ligne, colonne) == 16:
                                    send_message(addr, f"__GRILLEPLEINE__La grille est pleine ! match nul")
                                else:
                                    send_message(autre_addr, f"__INVALIDE__Entrez votre prochain coup :")

                                    

def send_message(addr, message):
    """_summary_
    Fonction chargée d'envoyer des messages au client en fonction des balises placées dans la fonction "mecanique jeu"
    
    Args:
        addr (_tuple_): _adresse du joueur courant_
        message (_string_): _designe le message à envoyer au client_
    """
       
    #Si le message commence par la balise "PCOUP" (Premier Coup), on envoie ce message uniquement au joueur courant      
    if message.startswith("__PCOUP__"):
        msg = message.split("__PCOUP__")
        s.sendto(msg[1].encode(), addr)
    
    #Si le message commence par la balise "COUP", on envoie ce message à tous les joueurs
    if message.startswith("__COUP__"):
        msg = message.split("__COUP__")
        for adresses in joueur:
            s.sendto(msg[1].encode(), adresses)
    
    if message.startswith("__GRILLEPLEINE__"):
        msg = message.split("__GRILLEPLEINE__")
        for adresses in joueur:
            s.sendto(msg[1].encode(), adresses)
           
    #Si le message commence par la balise "INVALIDE", on envoie ce message au joueur courant
    if message.startswith("__INVALIDE__"):
        msg = message.split("__INVALIDE__")
        s.sendto(msg[1].encode(), addr)
    
    #Si le message commence par la balise "new_name", on lui enverra le message de bienvenue 
    if message.startswith("__new_name__:"):
         msg = message.split("__new_name__:")
         s.sendto((msg[1]+ msg[2]).encode(), addr)
    
    #Si le message commence par la balise "NTOUR" (Non Tour), on envoie ce message au joueur non courant
    if message.startswith("__NTOUR__"):
        msg = message.split("__NTOUR__")
        s.sendto(msg[1].encode(), addr)
    
    #Si le message commence par la balise "Victoire", on envoie ce message à tous les joueurs
    if message.startswith("__VICTOIRE__"):
        msg = message.split("__VICTOIRE__")
        for adresses in joueur:
            s.sendto(msg[1].encode(), adresses)
        

def boucle_principal():
    """_summary_
    Fonction chargée de maintenir la boucle principal du jeu. Cette fonction s'assure d'utiliser les bonnes fonctions 
    selon si un client essaie d'entrer un nouveau nom ou si un client fait une tentative de coup
    """
    
    while True: 
        Message_entrant, addr = s.recvfrom(BUFFERSIZE)
        mss = Message_entrant.decode()
        if mss.startswith("__message__:"):
            message = mss.split("__message__:")
            mecanique_jeu(addr, message[1])
        elif mss.startswith("__new_name__:"):
            enregistre_joueur(addr, mss)
       
#Lancement du jeu
boucle_principal()
