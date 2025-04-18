import socket
import doctest
import os

ex_requete_http1="GET /page1.html HTTP/1.1\r\nHost: localhost\r\nAccept-Language: fr-FR,en;q=0.3\r\nUser-Agent: Mozilla/5.0 Firefox/98.0\r\n\r\n"
ex_requete_http2="GET /pages/index.html HTTP/1.1\r\nHost: localhost\r\nAccept-Language: fr\r\n\r\n"
ex_requete_http3="GET /autres_pages/toto.html HTTP/1.1\r\nHost: localhost\r\n\r\n"

IP = "127.0.0.1" # Definition de l'adresse IP du serveur
PORT = 8080 #Définition du port 
BUFFER_SIZE = 4096 #Définition du buffer size

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Definition du socket tcp
s.bind((IP,PORT)) #Associer l'adresse ip définie au port
s.listen() #Ecouter sur ce port

def decode_requete_http(requete) : #Fonction ayant pour but de décoder des requête http. Cette fonction retourne un tuple contenant l'url de la page et le dictionnaire contenant les métadonnées de celle ci
        """
        >>> a,b = decode_requete_http(ex_requete_http1)
        >>> a == "/page1.html"
        True
        >>> len(b)
        3
        >>> b["Host"] == "localhost"
        True
        >>> b["Accept-Language"] == "fr-FR,en;q=0.3"
        True
        >>> b["User-Agent"] == "Mozilla/5.0 Firefox/98.0"
        True
        """
        d = {
            
        }
        
        a = requete.split("\r\n")
        page = a[0].split(" ")[1]
        for i in range(1, len(a)-2):
            b = a[i].split(": ")
            d[b[0]] = b[1]
        
        return page, d

def get_reponse(url_page) : #Fonction ayant pour but de retourner une réponse HTTP selon l'url de la page passée en paramètre
        """
        >>> a = get_reponse("pages_serveur/fr/pages/index.html")
        >>> a == "HTTP/1.0 200 OK\\r\\nContent-Type:text/html\\r\\nContent-Length:73\\r\\n\\r\\n<!DOCTYPE html>\\n<html>\\n<body>\\n<h1>Voici index.html !</h1>\\n</body>\\n</html>\\r\\n"
        True
        >>> b = get_reponse("page_non_existante")
        >>> b == "HTTP/1.0 404 NotFound\\r\\nContent-Type:text/html\\r\\nContent-Length:177\\r\\n\\r\\n<!DOCTYPE html>\\n<html>\\n<head><title>404 Not Found</title></head><body>\\n<h1>Page non trouvée !!</h1>\\n<p>L'URL demandée n'a pas été trouvée sur ce serveur.</p></body>\\n</html>\\r\\n"
        True
        """
        try : 
            fichier = open(url_page, "r")
            content = fichier.read()
            length = os.path.getsize(url_page)
            return f"HTTP/1.0 200 OK\r\nContent-Type:text/html\r\nContent-Length:{length}\r\n\r\n{content}\r\n"
        except Exception : 
            file = open("pages_serveur/page404.html", "r")
            contenu = file.read()
            length = os.path.getsize("pages_serveur/page404.html")
            return f"HTTP/1.0 404 NotFound\r\nContent-Type:text/html\r\nContent-Length:{length}\r\n\r\n{contenu}\r\n"
        

def traite_requete(requete) : #Fonction ayant pour but de décoder la requête et de générer une réponse appropriée
        """
        >>> traite_requete(ex_requete_http2) == get_reponse("pages_serveur/fr/pages/index.html")
        True
        >>> traite_requete(ex_requete_http3) == get_reponse("pages_serveur/en/autres_pages/toto.html")
        True
        """
        a = decode_requete_http(requete)
        dico = a[1]
        
        if "Accept-Language" in dico.keys():
            cle = [dico["Accept-Language"]]
        else:
            cle = [""]
                
        url = a[0]
        
        if cle[0].startswith("fr"):
            b = "pages_serveur/fr" + url
            return get_reponse(b)
        else:
            return get_reponse("pages_serveur/en" + url)
    

#Boucle dont le but est d'accepter les différentes demandes de connexion au serveur
while True:
    s_conn, addr = s.accept()
    requete = s_conn.recv(BUFFER_SIZE).decode()
    print(f"Requête reçue:\n{requete}")
    reponse = traite_requete(requete)
    s_conn.send(reponse.encode())
    s_conn.close()



#http://127.0.0.1:8080/pages/nom_page
