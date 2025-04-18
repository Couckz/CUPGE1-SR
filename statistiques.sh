#!/bin/bash

function statistiques() {
    NBR_FICHIER=$(find $PWD -type f | wc -l) #Variable comptant le nombre de fichier dans le répertoire de travail
    NBR_FICHIER_VIDE=$(find $PWD -type f -empty | wc -l) #Variable comptant le nombre de fichiers vides dans le répertoire de travail
    NBR_FICHIER_CACHE=$(find $PWD -type f -name '.*' | wc -l) #Variable comptant le nombre de fichier comprenant un "." dans leurs expression (fichiers cachés) dans le répertoire de travail
    NBR_DOSSIER=$(find $PWD -type d | wc -l) #Variable comptant le nombre de dossier dans le répertoire de travail
    NBR_DOSSIER=$((NBR_DOSSIER - 1)) #Variable utilisée pour ne pas compter le répertoire principal dans la statistique
    NBR_DOSSIER_VIDE=$(find $PWD -type d -empty | wc -l) #Variable comptant le nombre de dossiers vides dans le répertoire de travail
    NBR_DOSSIER_CACHE=$(find $PWD -type d -name '.*' | wc -l) #Variable comptant le nombre de dossiers comprenant un "." dans leurs expression (dossiers cachés) dans le répertoire de travail
    NBR_FICHIER_JPEG=$(find $PWD -type f -name '*.jpg' | wc -l) #Variable comptant le nombre de fichiers comprenant un ".jpg" dans leurs expression (fichiers jpg) dans le répertoire de travail
    NBR_FICHIER_AVI=$(find $PWD -type f -name '*.avi' | wc -l) #Variable comptant le nombre de fichiers comprenant un ".avi" dans leurs expression (fichiers avi) dans le répertoire de travail
    NBR_FICHIER_PNG=$(find $PWD -type f -name '*.png' | wc -l) #Variable comptant le nombre de fichiers comprenant un ".png" dans leurs expression (fichiers png) dans le répertoire de travail
    NBR_FICHIER_MP4=$(find $PWD -type f -name '*.mp4' | wc -l) #Variable comptant le nombre de fichiers comprenant un ".mp4" dans leurs expression (fichiers mp4) dans le répertoire de travail
    NBR_FICHIER_MKV=$(find $PWD -type f -name '*.mkv' | wc -l) #Variable comptant le nombre de fichiers comprenant un ".mkv" dans leurs expression (fichiers mkv) dans le répertoire de travail
    NBR_FICHIER_PY=$(find $PWD -type f -name '*.py' | wc -l) #Variable comptant le nombre de fichiers comprenant un ".py" dans leurs expression (fichiers  python ) dans le répertoire de travail
    NBR_FICHIER_HTML=$(find $PWD -type f -name '*.html' | wc -l) #Variable comptant le nombre de fichiers comprenant un ".html" dans leurs expression (fichiers html) dans le répertoire de travail
    VIDEO=$((NBR_FICHIER_MKV + NBR_FICHIER_MP4 + NBR_FICHIER_AVI)) #Variable faisant la somme de tous les fichiers vidéos
    IMG=$((NBR_FICHIER_PNG + NBR_FICHIER_JPEG)) #Variable faisant la somme de tous les fichiers images
    TAILLE_MOINS_512KIO=$(find $PWD -type f -size -512k | wc -l) #Variable servant à déterminer le nombre de fichier ayant une taille inférieure à 512Ko
    TAILLE_PLUS_15MIO=$(find $PWD -type f -size +15M | wc -l) #Variable servant à déterminer le nombre de fichier ayant une taille supérieure à 15Mo
    PLUS_GROS_FICHIER=$(find $PWD -type f -printf "%s %p\n" | sort -n | tail -n 1 | awk '{print $2}') #Variable servant à déterminer le plus gros fichier (taille des fichiers placés dans l'ordre croissant puis sélection du dernier élement puis affichage de celui ci avec awk)


    #Teste sur le nombre d'argument passé en paramètre. Si celui ci est nul ou que l'argument fournit est égal à 1, nous sommes dans une configuration "peu de détail"
    if [ $# -eq 0 ] || [ $1 -eq 1 ]; then
        echo "Analyse de $PWD :"
        echo "    - $NBR_DOSSIER répertoire(s)"
        echo "    - $NBR_FICHIER fichier(s)"
        echo "    - taille totale : $(du -sh $PWD | awk '{print $1}')"
    fi

    #Test sur la valeur de l'argument passé en paramètre. Si celui ci vaut 2, nous sommes dans une configuration où l'on donnera un peu plus de détail que le cas précédent
    if [ $1 -eq 2 ]; then
        echo "Analyse de $PWD :"
        echo "    - $NBR_DOSSIER répertoire(s)"
        echo "        - $NBR_DOSSIER_VIDE répertoire(s) vide(s)"
        echo "        - $NBR_DOSSIER_CACHE répertoire(s) caché(s)"
        echo "    - $NBR_FICHIER fichier(s) dont"
        echo "        - $NBR_FICHIER_VIDE fichier(s) vide(s)"
        echo "        - $NBR_FICHIER_CACHE fichier(s) caché(s)"
        echo "    - taille totale : $(du -sh $PWD | awk '{print $1}')"
    fi

    #Test sur la valeur de l'argument passé en paramètre. Si celui ci vaut 3, nous sommes dans le cas où nous donnons le plus de détail à l'utilisateur
    if [ $1 -ge 3 ]; then
        echo "Analyse de $PWD :"
        echo "    - $NBR_DOSSIER répertoire(s)"
        echo "        - $NBR_DOSSIER_VIDE répertoire(s) vide(s)"
        echo "        - $NBR_DOSSIER_CACHE répertoire(s) caché(s)"
        echo "    - $NBR_FICHIER fichier(s) dont"
        echo "        - $NBR_FICHIER_VIDE fichier(s) vide(s)"
        echo "        - $NBR_FICHIER_CACHE fichier(s) caché(s)"
        echo "        - $TAILLE_MOINS_512KIO fichier(s) de moins de 512 kio"
        echo "        - $TAILLE_PLUS_15MIO fichier(s) de plus de 15 Mio"
        echo "        - le plus gros fichier est :"
        echo "             $PLUS_GROS_FICHIER"
        echo "       Il y a :"
        echo "          - $NBR_FICHIER_PY fichier(s) Python"
        echo "          - $IMG fichier(s) image"
        echo "          - $VIDEO fichier(s) vidéo"
        echo "    - taille totale : $(du -sh $PWD | awk '{print $1}')"
    fi
}
