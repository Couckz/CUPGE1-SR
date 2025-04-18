import struct
import doctest
import socket

ex_udp = b'\x00-\xd9\x9e\x00\x0eR\x8ccoucou'
ex_tcp = b'\x00-\xd7[\x00\x00\x17\x15\x00\x00\x04e\x86\xc6\ndg!By!\xaf\xff&\xfc\x19R\xcc\x18\xac|(coincoin'
ex_icmp = b'\x05\x04g\x90\x1a@\xc9\x01'
ex_ip = b"H\xf7\x00&[\x0cI\r\xe5\x01v5\xea\xd8\xa0\xe5L\xda\x86\x93\x0e\xa0\xed\xe8\x99\xc1G\xc0{P'\xc4cuicui"
ex_eth = b'R\x0c\xc7\x1d\xca578\x1fUk\x98\x08\x00coicoi'

ex_complet1 = b'Q\xf0\xdeG?\xf4\xa0\x18\x12f\xde\xd5\x08\x00H$\x00(\x85\xc2\x11\xcc\x83\x01\xf1\x94\xff\xfc\xbf\x067\x17\xd9\x86\xd4\x96\xbf\xdfdv$a\xae\x01\xd0\x90\n\x07\x1d\xfd\xdb\t3\xad'
ex_complet2 = b'\xb3\x82\x90ze\xe66?HJ#9\x08\x00Hu\x00G\\S\n{\r\x06\x0f\x93\x1f\xc9\xa5\xd0\xac\xea\xbc\xea\xc4\x13a\xdet>\xe1\x13\x9cJ\x8f\x1b\x03\x15\xf5\x83\x00\x00\x11L\x00\x00\r\xea\x80:\\\x9dJ\x9c)\xaf\xba\xcc){\xc0\x97\x83\xc4\xcd\xec3\xb4bravo !'
ex_complet3 = b"2\xa7\xa4\x97\xe3\x7fv\x17\x00\xaf{N\x08\x00H$\x000nu\x942\x05\x11\x857K\xf46\xb4K\x8a\xe8\xfb\xabt\x1f-\xff\xcd_b\xa0\x02\r\xa4\x03,\xeb\xe1\x00\x10?\x1dextra :o'"
ex = b'\xac\xd6E\xfd|\xcf\xbc\x1e\xf9\xc71\x8b\x08\x00Hj\x00(\xbc\xfd|\xd6\xa9\x01\xe5\xe7M\t\xe8m`$\xe9:\ra\x08\xc7\x0c\xd1\xc8U\xe8yxq\x06\x04\xe9G\xb4(3_'

#Fonctoin chargée de décoder les trames udp 
def decode_udp(data) :
    """
    >>> a = decode_udp(ex_udp)
    >>> len(a) == 2
    True
    >>> a[0] == "        +++ Paquet UDP +++\\n            Port source      : 45\\n            Port destination : 55710\\n            Longueur totale  : 14\\n"
    True
    >>> a[1].decode('utf-8') == "coucou"
    True
    """
    données = struct.unpack("!HHHH", data[:8])
    txt = data[8:]
    return f"        +++ Paquet UDP +++\n            Port source      : {données[0]}\n            Port destination : {données[1]}\n            Longueur totale  : {données[2]}\n",txt

#Fonction chargée de décoder les trames tcp
def decode_tcp(data) :
    """
    >>> a = decode_tcp(ex_tcp)
    >>> len(a) == 2
    True
    >>> a[0] == "        +++ Paquet TCP +++\\n            Port source      : 45\\n            Port destination : 55131\\n            Longueur en-tête : 8\\n"
    True
    >>> a[1].decode('utf-8') == "coincoin"
    True
    """
    données = struct.unpack("!HHLLH", data[:14])
    txt = data[32:]
    PB = données[4]
    LET = PB >> 12
    return f"        +++ Paquet TCP +++\n            Port source      : {données[0]}\n            Port destination : {données[1]}\n            Longueur en-tête : {LET}\n", txt

#Fonction chargée de décoder les trames icmp
def decode_icmp(data) :
    """
    >>> a = decode_icmp(ex_icmp)
    >>> a == "        +++ Paquet ICMP +++\\n            Type             : 5\\n"
    True
    """
    données = struct.unpack("!B", data[:1])
    
    return f"        +++ Paquet ICMP +++\n            Type             : {données[0]}\n"

#Fonction chargée de mettre au "bon format" les adresses IP 
def decode_adresse_IP(addr):
    """
    >>> decode_adresse_IP(2475088460) == "147.134.218.76"
    True
    """
    binaire = bin(addr)[2:].zfill(32)
    
    X = int(binaire[0:8], 2)
    Y = int(binaire[8:16], 2)
    Z = int(binaire[16:24], 2)
    T = int(binaire[24:32], 2)

    return f"{X}.{Y}.{Z}.{T}"

#Fonction chargée de décoder une trame ip 
def decode_ip(data) :
    """
    >>> a = decode_ip(ex_ip)
    >>> len(a) == 3
    True
    >>> a[0] == '    --- Paquet IP ---\\n        Version          : 4\\n        Longueur en-tête : 8\\n        Protocole        : 1\\n        Adresse source   : 234.216.160.229\\n        Adresse dest.    : 76.218.134.147\\n'
    True
    >>> a[1] == 1
    True
    >>> a[2].decode('utf-8') == "cuicui"
    True
    """
    données = struct.unpack("!BBHHHBBHLL", data[:20])
    PB1 = données[0]
    VERSION = PB1 >> 4
    LET = (72 % (2**4))
    txt = data[32:]
    return f"    --- Paquet IP ---\n        Version          : {VERSION}\n        Longueur en-tête : {LET}\n        Protocole        : {données[6]}\n        Adresse source   : {decode_adresse_IP(données[8])}\n        Adresse dest.    : {decode_adresse_IP(données[9])}\n",données[6],txt


#Fonction chargée de décoder une adresse mac
def decode_mac(data) :
    """
    >>> decode_mac(b'R\\x0c\\xc7\\x1d\\xca5') == "52:0c:c7:1d:ca:35"
    True
    """
    données = struct.unpack("!BBBBBB", data[:6])
    string=""
    for i in range(len(données)):
        var="%.2x" % données[i]
        string+=var
        string+=":" 
    
    return string[:-1]

#Fonction chargée de décoder une trame Ethernet
def decode_Ethernet(data) :
    """
    >>> a = decode_Ethernet(ex_eth)
    >>> len(a) == 3
    True
    >>> a[0] == '>>> Trame Ethernet <<<\\n    Adresse MAC Destination : 52:0c:c7:1d:ca:35\\n    Adresse MAC Source      : 37:38:1f:55:6b:98\\n    Protocol                : 2048\\n'
    True
    >>> a[1] == 2048
    True
    >>> a[2].decode('utf-8') == "coicoi"
    True
    """
    données = struct.unpack("!6B6BH", data[:14])
    txt = data[14:]
    Source=data[:6]
    Destination=data[6:12]
    return f">>> Trame Ethernet <<<\n    Adresse MAC Destination : {decode_mac(Source)}\n    Adresse MAC Source      : {decode_mac(Destination)}\n    Protocol                : {données[12]}\n", données[12],txt

#Fonction chargée de décoder l'entierté d'une trame 
def decode_trame(data) :
    a = decode_Ethernet(data)
    b = decode_ip(a[2])
    
    if a[1] == 2048:
        if b[1] == 1:
            print(f"{a[0]}{decode_ip(a[2])[0]}{decode_icmp(b[2])}")
        elif b[1] == 6:
            print(f"{a[0]}{decode_ip(a[2])[0]}{decode_tcp(b[2])[0]}data : {decode_tcp(b[2])[1]}")
        elif b[1] == 17:
            print(f"{a[0]}{decode_ip(a[2])[0]}{decode_udp(b[2])[0]}data : {decode_udp(b[2])[1]}")
            
    

if __name__ == "__main__" :
    doctest.testmod(verbose=True)
    print("ex_complet1 :")
    decode_trame(ex_complet1)
    print("ex_complet2 :")
    decode_trame(ex_complet2)
    print("ex_complet3 :")
    decode_trame(ex_complet3)