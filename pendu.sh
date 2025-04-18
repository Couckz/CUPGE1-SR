#!/bin/bash

DICT=$1
FICHIER=$HOME/$DICT


if [ $# -eq 0 ]; then
    echo -e  "pendu.sh s'exécute avec un argument :\n    pendu.sh nom_fichier\noù \"nom_fichier\" est le dictionnaire pour le choix des mots"
else

    if ! [ -e $DICT ]; then
        echo "\"$DICT\" n'est pas un nom de fichier existant" 
    elif [ -d $DICT ]; then
        echo "le fichier que vous avez entré est un dossier"
    fi

    if [ $# -eq 1 ]; then
        if [ -e $DICT ] && [ -f $DICT ]; then
            LETTRES_TESTEES=""
            LINES=$(cat $1)
            NB_TENTATIVES=10
            LETTRES_RESTANTES="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            
            function choisi_mot() {
                nb_lignes=$(wc -l < "$DICT" | tr -d ' ')
                nb_aleatoire=$((RANDOM % $nb_lignes + 1)) 
                counter=0

                for MOT in $LINES; do
                    ((counter++))
                    if [ $counter -eq $nb_aleatoire ]; then
                        MOT_A_TROUVE=$MOT
                    fi
 	            done
                
                LETTRE_DANS_MOT=$(echo -n $MOT_A_TROUVE | wc -m)
                compteur=0
                MOT_DEVINE=""
                while ! [ $compteur -eq $LETTRE_DANS_MOT ]; do
                    ((compteur++))
                    MOT_DEVINE+="_"
                done

            }
            
            LETTRES_TROUVEES=""
            function teste_lettre() { 

                    
                        if [[ $MOT_A_TROUVE =~ $1 ]]; then
                            LETTRES_TROUVEES+=$1
                            LETTRES_TESTEES+=" $1"
                            LETTRES_RESTANTES=$(echo "$LETTRES_RESTANTES" | tr -d "$1")
                            MOT_DEVINE=$(echo "$MOT_A_TROUVE" | sed "s/[^$LETTRES_TROUVEES]/_/g")
                        
                        else
                            ((NB_TENTATIVES--))
                            LETTRES_TESTEES+=" $1"
                            LETTRES_RESTANTES=$(echo "$LETTRES_RESTANTES" | tr -d "$1")
                        fi
                    
                
            }

            function affiche_pendu() { 
                if [ $NB_TENTATIVES -eq 10 ]; then
                echo -e "******************************\n\n\n\n\n\n\n\n"
                if [ $count -eq 1 ]; then
                ((count++))
                echo -e "Lettres testées : $LETTRES_TESTEES\n"
                else
                echo -e "Lettres testées : $LETTRES_TESTEES\n"
                fi
                echo "$MOT_DEVINE"
                echo -e "$MOT_A_TROUVER"
                elif [ $NB_TENTATIVES -eq 9 ]; then
                echo -e "******************************\n\n\n\n\n\n\n___ ___\n"
                echo -e "Lettres testées : $LETTRES_TESTEES\n"
                echo "$MOT_DEVINE"
                echo -e "$MOT_A_TROUVER"
                
                elif [ $NB_TENTATIVES -eq 8 ]; then
                echo -e "******************************\n\n\n   |\n   |\n   |\n   |\n___|___\n"
                echo -e "Lettres testées : $LETTRES_TESTEES\n"
                echo "$MOT_DEVINE"
                echo -e "$MOT_A_TROUVER"
                
                elif [ $NB_TENTATIVES -eq 7 ]; then
                echo -e "******************************\n\n    _____\n   |\n   |\n   |\n   |\n___|___\n"
                echo -e "Lettres testées : $LETTRES_TESTEES\n"
                echo "$MOT_DEVINE"
                echo -e "$MOT_A_TROUVER"
                
                elif [ $NB_TENTATIVES -eq 6 ]; then
                echo -e "******************************\n\n    _____\n   |     |\n   |\n   |\n   |\n___|___\n"
                echo -e "Lettres testées : $LETTRES_TESTEES\n"
                echo "$MOT_DEVINE"
                echo -e "$MOT_A_TROUVER"
                
                elif [ $NB_TENTATIVES -eq 5 ]; then
                echo -e "******************************\n\n    _____\n   |     |\n   |     O\n   |\n   |\n___|___\n"
                echo -e "Lettres testées : $LETTRES_TESTEES\n"
                echo "$MOT_DEVINE"
                echo -e "$MOT_A_TROUVER"
                
                elif [ $NB_TENTATIVES -eq 4 ]; then
                echo -e "******************************\n\n    _____\n   |     |\n   |     O\n   |     |\n   |\n___|___\n"
                echo -e "Lettres testées : $LETTRES_TESTEES\n"
                echo "$MOT_DEVINE"
                echo -e "$MOT_A_TROUVER"   
                
                elif [ $NB_TENTATIVES -eq 3 ]; then
                echo -e "******************************\n\n    _____\n   |     |\n   |     O\n   |    /|\n   |\n___|___\n"
                echo -e "Lettres testées : $LETTRES_TESTEES\n"
                echo "$MOT_DEVINE"
                echo -e "$MOT_A_TROUVER"
                
                elif [ $NB_TENTATIVES -eq 2 ]; then
                echo -e "******************************\n"
                echo -e '    _____'
                echo -e '   |     |'
                echo -e '   |     O'
                echo -e '   |    /|\'
                echo -e '   |'
                echo -e "___|___\n"
                echo -e "Lettres testées : $LETTRES_TESTEES\n"
                echo "$MOT_DEVINE"
                echo -e "$MOT_A_TROUVER"
                
                elif [ $NB_TENTATIVES -eq 1 ]; then
                echo -e "******************************\n"
                echo -e '    _____'
                echo -e '   |     |'
                echo -e '   |     O'
                echo -e '   |    /|\'
                echo -e '   |    /'
                echo -e "___|___\n"
                echo -e "Lettres testées : $LETTRES_TESTEES\n"
                echo "$MOT_DEVINE"
                echo -e "$MOT_A_TROUVER"
                
                elif [ $NB_TENTATIVES -eq 0 ]; then
                echo -e "******************************\n\n    _____\n   |     |\n   |     O\n   |    /|\  \n   |    / \ \n___|___\n"
                echo -e "PERDU :("
                echo -e "Le mot à trouver était : $MOT_A_TROUVE"
                fi
                

            }
        
            count=1
            function jeu_pendu() { 

                while [[ $NB_TENTATIVES -gt 0 && "$MOT_DEVINE" != "$MOT_A_TROUVE" ]]; do
                    
                    
                    echo -e "Choisissez une lettre : " 
                    read lettre
                    
                



                    if [[ "$MOT_DEVINE" == "$MOT_A_TROUVE" ]]; then 
                        echo "GAGNE !!"
                        return 0  
                    fi

                    if ! [[ $LETTRES_RESTANTES =~ $lettre ]]; then
                        echo -e "Lettre choisie incorrecte (ou déjà testée) !\n"
                        echo -e "$MOT_DEVINE\n"
                        continue  
                    fi

                    teste_lettre "$lettre"
        
                    if [[ "$MOT_DEVINE" == "$MOT_A_TROUVE" ]]; then 
                        echo "GAGNE !!"
                        return 0  
                    elif [[ $NB_TENTATIVES -eq 0 ]]; then 
                        echo -e "******************************\n"
                        echo -e '    _____'
                        echo -e '   |     |'
                        echo -e '   |     O'
                        echo -e '   |    /|\'
                        echo -e '   |    / \'
                        echo -e "___|___\n"
                        echo -e "PERDU :("
                        echo -e "Le mot à trouver était : $MOT_A_TROUVE"
                        return 1
                    fi

                    affiche_pendu  
                done
                

                
            }


            
            
            choisi_mot
            affiche_pendu 
            jeu_pendu
            
            
            

        fi
    fi

fi
