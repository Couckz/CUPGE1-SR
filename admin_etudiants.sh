#!/bin/bash

liste=$1 #Variable servant à désigner la liste fournie en paramètre
espace=$2 #Variable servant à désigner le répertoire dans lequel les dossier seront crées
RANDOM=/dev/urandom
export LC_ALL=C #Ligne pour éviter les problèmes d'encodages avec la commande tr (spécifique à macOS) 

#Ces test servent à déterminer si le bon nombre d'argument a été fournit (le premier test permet d'identifier si deux arguments ont bien été passés)
if [ $# -eq 2 ]; then
    #Ce test permet de vérifier l'existante du fichier passé en paramètre
    if ! [ -e $liste ]; then
            echo "$liste n'est pas un nom de fichier existant" 
    #Ce test permet de vérifier l'existante du dossier passé en paramètre
    elif ! [ -e $espace ]; then
            echo "$espace n'est pas un nom de dossier existant" 
    #Ce test permet de vérifier que le fichier passé en paramètre n'est pas un dossier
    elif [ -d $liste ]; then
        echo "le fichier que vous avez entré est un dossier"
    #Ce test permet de vérifier que le dossier passé en paramètre n'est pas un fichier
    elif [ -f $espace ]; then
        echo "le dossier que vous avez entré est un fichier"
    fi 

    #Dans le cas où l'on a bien un fichier et un dossier passé en paramètre, on peut exécuter le reste du code
    if [ -f $liste ] && [ -d $espace ]; then
        #Lecture ligne par ligne des lignes du fichier passé en paramètre
        cat $liste | while read LINES ; do 
            #Les instructions suivantes permettent de supprimer tout signe de ponctuation pouvant être présent dans les noms des étudiants. La variable "letters" désigne les deux premières lettres du prénom
            NOM=$(echo "$LINES" | cut -d';' -f1)
            NOM1=$(echo $NOM | tr -d ' ')
            NOM2=$(echo $NOM1 | tr -d "'" )
            PRENOM=$(echo "$LINES" | cut -d';' -f2)
            LETTERS=$(echo $PRENOM | cut -c 1-2) 
            #Dans le cas où la longueur du nom est inférieur ou égal à 7, nous créeons un repértoire portant les deux première lettres du prénom suivit du nom complet. Et nous créeons plusieurs dossiers dans ce répertoire ainsi qu'un fichier dans lequel sera contenu un mot de passe généré aléatoirement
            if [ ${#NOM} -le 7 ]; then
                PSEUDO="$LETTERS$NOM2"
                mkdir $espace/$PSEUDO
                mkdir $espace/$PSEUDO/Documents
                mkdir $espace/$PSEUDO/Images
                touch $espace/$PSEUDO/mot_de_passe.txt
                 MDP=""
                MDP+=$(cat /dev/urandom | tr -dc 'bcdfghjklmnpqrstvwxyz' | head -c 1) 
                MDP+=$(cat /dev/urandom | tr -dc 'aeiou' | head -c 1)                
                MDP+=$(cat /dev/urandom | tr -dc 'bcdfghjklmnpqrstvwxyz' | head -c 1) 
                MDP+=$(cat /dev/urandom | tr -dc 'aeiou' | head -c 1)                
                MDP+=$(cat /dev/urandom | tr -dc '1234567890' | head -c 4)           

                echo "$MDP" > "$espace/$PSEUDO/mot_de_passe.txt"
            #Si ce n'est pas le cas, nous éxecutons les même actions que dans le cas précédent mais nous sélectionnerons seulement les 7 première lettres du nom
            else
                NOM=$(echo "$LINES" | cut -d';' -f1)
                NOM1=$(echo $NOM | tr -d ' ')
                NOM2=$(echo $NOM1| tr -d "'")
                NOM3=$(echo $NOM2 | cut -c 1-7)
                PSEUDO="$LETTERS$NOM3"
                mkdir $espace/$PSEUDO
                mkdir $espace/$PSEUDO/Documents
                mkdir $espace/$PSEUDO/Images
                touch $espace/$PSEUDO/mot_de_passe.txt
                 MDP=""
                MDP+=$(cat /dev/urandom | tr -dc 'bcdfghjklmnpqrstvwxyz' | head -c 1) 
                MDP+=$(cat /dev/urandom | tr -dc 'aeiou' | head -c 1)                
                MDP+=$(cat /dev/urandom | tr -dc 'bcdfghjklmnpqrstvwxyz' | head -c 1) 
                MDP+=$(cat /dev/urandom | tr -dc 'aeiou' | head -c 1)                
                MDP+=$(cat /dev/urandom | tr -dc '1234567890' | head -c 4)           
                echo "$MDP" > "$espace/$PSEUDO/mot_de_passe.txt"
            fi

        done

        

    fi 
    #Dans le cas où le nombre d'argument n'est pas le bon, nous renvoyons la documentation de la commande
    else
        echo "admin_etudiants.sh s'utilise avec \"admin_etudiants.sh liste_nom_etudiants dossier_parent\""
    fi