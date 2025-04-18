#!/bin/bash

function todo() { 
	TACHES=$HOME/.todo_list  #Liste des tâches de la todo list
	STOCK=$HOME/.stock_list.txt  #Fichier intermediaire qui sera utilisé pour la modification de la todo list
	  

	    #Test pour vérifier que l'utilisateur a bien rentré le bon nombre d'argument
           if [ $# -eq 0 ]; then
	                echo "La commande 'todo' s'exécute avec 'todo (add | done | list) (arguments)'"
	                else
				#Si l'utilisateur entre comme premier argument le mot "add" et s'il n'oublie pas de spécifier le numéro "n" de la tâche 
				#Alors nous transferons les n-1 première lignes de la todo list dans le fichier "stock" puis nous ajoutons la tâche en position "n". Après cela, nous transférons les lignes restantes dans le fichier "stock" puis nous remplaçons le contenu de "tache" par le contenu de ce fichier.
	            if [ "$1" = "add" ]; then
	                if [ $# -eq 1 ]; then
	                echo "La commande 'todo add' s'exécute avec 'todo add numero_tache action_a_ajouter'"
	                else
		            NUMERO=$2
      			    echo "La tâche \"${@:3}\" a été ajoutée en position $NUMERO." 
      			    head -n $(($NUMERO - 1)) "$TACHES" > "$STOCK" 
      			    echo "${@:3}" >> "$STOCK" 
      			    tail -n +$(($NUMERO)) "$TACHES" >> "$STOCK" 
      			    cat "$STOCK" > "$TACHES" 
      			    fi
    		
  
			#Si l'utilisateur entre comme premier argument le mot "list", nous affichons le contenu de la todo list stockée dans le fichier "tache"
	        elif [ $1 = list ]; then 
 	            for VAR in $TACHES; do
 		        	cat "$TACHES" | nl -s " - " -w1
 	            done

			#Si l'utilisateur entre comme premier argument le mot "done" et s'il n'oublie pas de spécifier le numéro "n" de la tâche 
			#Alors nous transferons les n-1 première lignes de la todo list dans le fichier "stock" puis nous supprimons la tâche en position "n". Après cela, nous transférons les lignes restantes dans le fichier "stock" puis nous remplaçons le contenu de "tache" par le contenu de ce fichier.
	        elif [ $1 = done ]; then 
	            if [ $# -eq 1 ]; then
	            echo "La commande 'todo done' s'exécute avec 'todo done numero_tache'"
	            else
 	            NUMERO_TACHE=$2
 	            echo "La tâche $NUMERO_TACHE ($(sed -n "${NUMERO_TACHE}p" "${TACHES}")) est faite !"
 	            head -n $(($NUMERO_TACHE-1)) $TACHES > $STOCK 
 	            tail -n +$(($NUMERO_TACHE+1)) $TACHES >> $STOCK
 	            cat "$STOCK" > "$TACHES" 
 	            fi
 	   
			#Dans le cas où l'utilisateur un argument incorrecte (hors "add", "done" et "list" nous lui renvoyons la documentation de la commande)
 	        else 
 	           echo "La commande 'todo' s'exécute avec 'todo (add | done | list) (arguments)'"
 	        fi
 	        fi
 	  
	}
	

