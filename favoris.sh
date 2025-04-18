#/!bin/bash

TEMP=$HOME/.temporaire.txt #Fichier intermediaire servant à effectuer les modifications sur la liste de raccourcis
FAV=$HOME/.favoris_bash  #Fichier contenant les raccourcit

#Fonction servant à sauvegarder des raccourcit
function S() {
        if [ $# -eq 0 ]; then
                echo "La commande 'S' s'exécute avec 'S nom_raccourci'"
                else
        

                if ! grep -q "$1" $FAV; then
                        echo "$1 -> $PWD" >> $FAV
                        echo -e "Le répertoire $PWD est sauvegardé dans vos favoris.\n  -> raccourci : $1"
                            
                else
                        echo -e "Le raccourci '$1' existe déja :\n  $(grep "^$1" $FAV)"
                fi

        fi
                

              
        
}

#Fonction servant à changer de répertoire de travail en fonction du raccourci passé en paramètre
function C() {
        #Test sur le nombre d'argument si l'utilisateur ne rentre pas de raccourcit un message d'erreur est affiché
        if [ $# -eq 0 ]; then
                echo "La commande 'C' s'exécute avec 'C nom_raccourci'"
                else
                        #Test sur le contenu du fichier contenant les raccorucit. Si le fichier contient le nom de raccourcit passé en paramètre, on se déplace dans le répertoire associé
                        if grep -q "^$1" $FAV; then
                                DEBUT=$(grep "^$1" $FAV)
                                REPERTOIRE=$(echo "$DEBUT" | cut -d' ' -f3)
                                cd $REPERTOIRE
   
                                
                        else
                                echo "Le raccourci '$1' n'existe pas."
             fi
        fi

        
}

#Fonction servant à supprimer des raccourcit
function R() {
        #Test sur le nombre d'argument. Si l'utilisateur ne rentre aucun argument, un message d'erreur est afffiché
        if [ $# -eq 0 ]; then
                echo "La commande 'R' s'exécute avec 'R nom_raccourci'"
                else
                        #Test sur le contenu du fichier contenant les raccorucit. Si le fichier contient le nom de raccourcit passé en paramètre, on supprime le raccourci passé en paramètre
                        if grep -q "^$1" $FAV; then
                                raccourci=$1
 	                        grep -v $raccourci $FAV > $TEMP #Utilisation du fichier temporaire pour modifier la liste de raccourcit (supprimer le raccourci passé en paramètre)
                                cat $TEMP > $FAV
                                echo "Le favori \"$1\" a été supprimé de votre liste."
   
                                
                        else
                                echo "Le raccourci '$1' n'existe pas."
             fi
        fi
}

#Fonction servant à afficher la liste de raccourcit
function L() {
        #Test sur le nombre d'argument, si l'utilisateur passe en paramètre une lettre (ou suite de lettres), nous afficherons la liste des raccourcit commençant par cette suite de lettres
        if [ $# -eq 1 ]; then
        grep "^$1" $FAV
        else
        #Si l'utilisateur ne spécifie aucun argument, on affiche tout le contenu de la liste de raccourcit ligne par ligne
        cat $FAV | while read LIGNES ; do 
 	        echo $LIGNES
 	done

        fi
        
}