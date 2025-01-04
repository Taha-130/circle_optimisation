#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''jeu au tour par tour dont le but du jeu est
d’occuper la plus grande aire coloriée avec sa couleur. '''

# Imports ---------------------------------------------------------------------
from upemtk import *
from time import *
from math import pi
from math import sqrt
from random import *
from functools import lru_cache


# Fonctions -------------------------------------------------------------------
@lru_cache(maxsize=None)
def distance(x1, y1, x2, y2):
    """
    Calcule la distance entre deux points (coordonnées passées sous forme de scalaires).
    """
    return int(round(sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)))

def distance_wrapper(lst1, lst2):
    """
    Wrapper pour convertir des listes en tuples et appeler la fonction distance.
    """
    x1, y1 = lst1
    x2, y2 = lst2
    return distance(x1, y1, x2, y2)


def point_place(coordonnees, rayon, couleur, sauvegarde):
    """
    Prends en paramètres les coordonnées d'un point et sa couleur,
    suivit d'une liste contenant aussi des points et différentes données,
    puis renvoie True si le point est mal placé, c'est-a-dire si
    il dépasse les limites ou si il est trop proche des autre points
    de couleurs différentes, renvoie False sinon.
    >>> point_place(100, 300, 'red', [[300, 295, 50, 7854, 'blue', '6']])
    False
    >>> point_place(100, 300, 'red', [[388, 295, 50, 7854, 'red', '6'], [100, 295, 50, 7854, 'blue', '5']])
    True     à changer
    """
    """
    Vérifie si un point est mal placé.
    """
    x, y = coordonnees
    if y < 50 + rayon or x < rayon or y > 600 - rayon or x > 800 - rayon:
        return True

    for elt in sauvegarde:
        if elt[4] == 'white':
            continue
        if distance_wrapper(coordonnees, elt[0]) < elt[2] + rayon and couleur != elt[4]:
            return True
    return False

def surface(sauvegarde):
    """
    Calcule le score des deux camps
    """
    surface_totale_green=0
    surface_totale_red=0
    for i in range(len(sauvegarde)):
        if sauvegarde[i][4] == 'red':
            surface_totale_red += sauvegarde[i][3]
        if sauvegarde[i][4] == 'green':
             surface_totale_green += sauvegarde[i][3]
    return[surface_totale_red, surface_totale_green]


def division_cercle(coordonnees, sauvegarde, couleur):
    """
    Divise une boule ennemie si les coordonnées sont dedans.
    """
    x1, y1 = coordonnees
    for elt in sauvegarde:
        if elt[4] in {'white', 'black'}:
            continue
        if distance_wrapper(coordonnees, elt[0]) < elt[2] and couleur != elt[4]:
            r = elt[2]
            r2 = distance_wrapper(coordonnees, elt[0])
            r1 = r - r2
            couleur = elt[4]

            x, y = elt[0]
            cercle(x, y, elt[2] + 2, couleur='white', remplissage='white', epaisseur=0)
            sauvegarde.remove(elt)

            sauvegarde.append([(x1, y1), cercle(x1, y1, r1, remplissage=couleur), r1, int(round(pi * (r1 ** 2))), couleur])
            sauvegarde.append([(x + r2, y + r2), cercle(x + r2, y + r2, r2, remplissage=couleur), r2, int(round(pi * (r2 ** 2))), couleur])
            return sauvegarde
    return True

            
def tour(choix, max_delay, couleur, sauvegarde, budget):
    """
    Partie secondaire du main(), ne peut surement qu'être utilisé avec cette dernière
    """

    #attente de touche, servant au variantes "Terminaison" et "Scores"
    evenement = attente_clic_ou_touche()
    if evenement[2] == 'Touche':
        t = evenement[1]
        if choix["Terminaison"] and t =='f':
            sauvegarde[0][1] = t
            print("Le nombres de tours passera à 10 après ce tour\n")
            
        elif choix["Scores"] and t =='s':
            surf = surface(sauvegarde)
            print("Score rouge : " + str(surf[0]))
            print("Score vert : " + str(surf[1]))
            print()
        evenement = attente_clic()
            
    x = evenement[0]
    y = evenement[1]
    r = 50

    #Si on clique à l'intérieur d'une boule enemie, division
    if division_cercle((x, y), sauvegarde, couleur) != True:
        return budget

    #Test si les règles sont respectées  
    if time() > max_delay or point_place((x, y), 50, couleur, sauvegarde):
        txt = texte(0, 0, "tour passé")
        sauvegarde.append([(0, 0), 0, 0, 0, couleur])
        return budget
    
    #partie différente qui sert surtout pour la variante "Taille des boules"
    if choix["Taille des boules"]:
        
        r = int(input("Avec quel rayon ? "))
        print() #pour la lisibilité
        
        for elt in sauvegarde:
            if elt[4] == 'white':
                continue
            if r > 200 or point_place((x, y), r, couleur, sauvegarde):
                txt = texte(0, 0, "tour passé")
                sauvegarde.append([(0, 0), 0, 0, 0, couleur])
                return budget
            
        if budget <= 0 or r > budget:
            txt = texte(400, 300, "Pas assez de budget", taille="50", police="Monaco", ancrage="center")
            mise_a_jour()
            sleep(2)
            efface(txt)
            sauvegarde.append([(0, 0), 0, 0, 0, couleur])
            return budget

        budget -= r
        sauvegarde.append([(x, y), cercle(x, y, r, remplissage=couleur), r, int(round(pi*(r*r))), couleur])
        return budget
    
    
    sauvegarde.append([(x, y), cercle(x, y, r, remplissage=couleur), r, int(round(pi*(50*50))), couleur])
    return


#Programme IA ----------------------------------------------------------------------------          
def division_ia(couleur, sauvegarde):
    """
    Division d'une boule ennemie aléatoire dans sauvegarde
    """
    boule_div = choice(sauvegarde)
    if couleur == "red":
        while boule_div[4] != "green" or boule_div[2] == 0:
            boule_div = choice(sauvegarde)
    if couleur == "green":
        while boule_div[4] != "red" or boule_div[2] == 0:
            boule_div = choice(sauvegarde)
                
    x = randint(int(boule_div[0][0]-boule_div[2]),int(boule_div[0][0]+boule_div[2]))
    y = randint(int(boule_div[0][0]-boule_div[2]),int(boule_div[0][0]+boule_div[2]))
    division_cercle((x, y), sauvegarde, couleur)
        
    
def tour_ia(sauvegarde, choix, couleur, budget, nombre_tour):
    """
    Simule le tour qu'une IA ferait. Il y a une chance que,
    si la surface de l'IA est plus grande, elle divise une boule adverse.
    Il y a aussi une fine chance que l'IA rate et passe son tour.
    Sinon l'IA va placer ses Boules là où c'est possible de manière aléatoire.
    """
    if budget == 0:
        division_ia(couleur, sauvegarde)
        return budget

    if nombre_tour>5 and randint(1,3) == 2 :
        surf = surface(sauvegarde)
        if couleur == "red":
            surface_IA = surf[0]
            surface_enemi = surf[1]
        else:
            surface_IA = surf[1]
            surface_enemi = surf[0]
        
        if surface_IA<=surface_enemi:
            pass
        else:
            division_ia(couleur, sauvegarde)
            return budget
    
    if randint(1,2004) == 2004:
        texte_e = texte(0, 0, "tour IA passé")
        mise_a_jour()
        sleep(0.5)
        efface(texte_e)
        sauvegarde.append([(0, 0), 0, 0, 0, couleur])
        return budget
    
    if choix["Taille des boules"]:
        if budget < 81:
            rayon = budget
        else:
            rayon = randint(25,80)
    else:
        rayon = 50
        
    points_possibles = {
    (i, j)
    for i in range(50, 800, (rayon // 2) + 1)
    for j in range(100, 600, (rayon // 2) + 1)
    if not point_place((i, j), rayon, couleur, sauvegarde)
    }

                
    points_possibles_en = set()
    if couleur == "red":
        cou_en = "green"
    else:
        cou_en = "red"
    for i in range(50,800,(rayon//2)+1):
        for j in range(100,600,(rayon//2)+1):
            if point_place((i, j), rayon, cou_en, sauvegarde) != True:
                points_possibles_en.add((i, j))
    
    liste_point_placable = list(points_possibles&points_possibles_en)
    #L'Union des points plaçables par l'un et pas l'autre donne l'ensemble des points où il n'y a aucune boule
    #Mais si il n'y a pas de points où il n'y a aucune boule, on prends là où il a des boules alliées
    if len(liste_point_placable) == 0:
        liste_point_placable = list(points_possibles)
                
    if len(liste_point_placable) == 0:
        division_ia(couleur, sauvegarde)
        return budget
    
    else:
        x, y = choice(liste_point_placable)
    
    if choix["Taille des boules"]:
        budget -= rayon
    sauvegarde.append([(x, y), cercle(x, y, rayon, remplissage=couleur), rayon, int(round(pi*(rayon*rayon))), couleur])
    sleep(0.5)
    return budget
    
                
#Programme principal ---------------------------------------------------------------------            
def main(choix):
    #Demande à l'utilisateur de ses préférences
    nombre_tour = int(input("Combien de tours souhaitez vous ? (un clic, un tour): "))
    print() #pour la lisibilité
    if nombre_tour%2!=0:
        nombre_tour+=1
    if choix["Sablier"] :
        temps_dispo = int(input("Combien de temps souhaitez vous pour jouer ? (en secondes): "))
        print() #pour la lisibilité
    else:
        temps_dispo = 600 #on impose tout de même un max de 10 minutes
        
    #Création de la fenetre et d'un message pour attendre le lancement du jeu
    rectangle(0, 0, 800, 600, remplissage="white")
    rectangle(0, 0, 800, 50, remplissage="purple")
    texte(350, 20,"Batailles des boules", ancrage="center")
    txt = texte(400, 300, "READY?", taille="50", police="Monaco", ancrage="center")
    attente_clic()
    efface(txt)

    #Initialisation de variables
    txt = 0
    sauvegarde=[[(0, 0), 0, 0, 0, "red"], [(0, 0), 0, 0, 0, "green"]]
    if nombre_tour>=50:
        budget1 = 1500
        budget2 = 1500
    elif nombre_tour>=30:
        budget1 = 1000
        budget2 = 1000
    elif nombre_tour>=15:
        budget1 = 500
        budget2 = 500
    else:
        budget1 = 250
        budget2 = 250

    #Si l'utilisateur à choisi la variante "Obstacles", création de 3 obstacles
    if choix["Obstacles"]:
        for i in range(3):
            a = randint(300, 700)
            b = randrange(200, 500)
            rayon = randrange(100)
            sauvegarde.append([(a, b), cercle(a, b, rayon, remplissage='black'), rayon, 0, 'black'])
    
    #Début de la boucle du jeu 
    while nombre_tour>=1:
        now = time()
        max_delay = now + temps_dispo
        
        if nombre_tour%2==0: #Chaque joueur joue un tour sur deux
            txt2 = texte(540, 0, "joueur rouges")
            if choix["IAVSIA"] :
                budget1 = tour_ia(sauvegarde, choix, "red", budget1, nombre_tour)
            else:
                budget1 = tour(choix, max_delay, "red", sauvegarde, budget1)
            nombre_tour -= 1
            
        else:
            txt2 = texte(540, 0, "joueur verts")
            if choix["JVSIA"] or choix["IAVSIA"]:
                budget2 = tour_ia(sauvegarde, choix, "green", budget2, nombre_tour)
            else:
                budget2 = tour(choix, max_delay, "green", sauvegarde, budget2)
            nombre_tour -= 1

        #Test servant à la variante "Terminaison", tours mis a 10 si f est tapé    
        if sauvegarde[0][1] == 'f' and nombre_tour > 10:
            nombre_tour = 10
            print("Vous avez fixé le nombres de tours restant à 10\n")
            print() #pour la lisibilité
            sauvegarde[0][1] = 0
        elif sauvegarde[0][1] == 'f' and nombre_tour<=10:
            print("Le nombre de tours ne peux pas être fixé à 10\n")
            sauvegarde[0][1] = 0
            
        #effacement de textes nuisibles, et mise à jour
        efface(txt)
        efface(txt2)
        mise_a_jour()

    #Lorsque le compteur atteint 0, Fin de la boucle
    #Après la fin de la boucle, calcul des surface remplies
    surf = surface(sauvegarde)
    surface_totale_red = surf[0]
    surface_totale_green = surf[1]
    
    
    
    #Permet d'insérer le classement de la partie dans un fichier classement.txt
    if choix["JVSIA"]:
        nom = input("Entrer votre nom: ")
        print() #pour la lisibilité
        while ',' in nom:
            print("Ne mettez pas de virgule s'il vous plaît")
            nom = input("Entrer votre nom: ")
            print() #pour la lisibilité
            
        with open("classement.txt", "a") as f:
            f.write(nom + "," + str(surface_totale_red) + "\n")
            
        scores = []
    
        with open("classement.txt", "r") as f:
            for line in f:
                # Séparer le nom d'utilisateur et le score
                username, score = line.strip().split(",")
                scores.append((username, int(score)))
            
        scores.sort(key=lambda x: x[1], reverse=True)
        scores = scores[:5]
        # Afficher les scores
        print("Voici le classement des meilleurs scores:\n")
        for i, (username, score) in enumerate(scores):
            print(f"{i+1}. {username} : {score}")
    
    

    #Temps de répit pour que l'utilisateur voit le résultat final puis effacage de la fenêtre
    sleep(3)
    efface_tout()
    rectangle(0, 0, 800, 600, remplissage="white")

    #Calcul et affichage du gagnant
    if surface_totale_green<surface_totale_red:
        texte(400, 300, "LE JOUEUR DES BOULES ROUGES A GAGNÉ", taille="25", police="Monaco", ancrage="center")
    elif surface_totale_green==surface_totale_red:
        texte(400, 300, "ÉGALITÉ", taille="100", police="Monaco", ancrage="center")
    else:
        if choix["JVSIA"]:
            texte(400, 300, "L'IA A GAGNÉ", taille="25", police="Monaco", ancrage="center")
        else:
            texte(400, 300, "LE JOUEUR DES BOULES VERTES A GAGNÉ", taille="25", police="Monaco", ancrage="center")
    
    mise_a_jour()

    #Temps de répit puis fermeture de la fenêtre au clic de l'utilisateur
    sleep(2)
    attente_clic()
    ferme_fenetre()
    

#Menu de début ---------------------------------------------------------------------            
def menu():
    """
    Menu de début servant au choix des variantes.
    """
    choix = {"JVSIA": False, "IAVSIA": False, "Sablier" : False, "Scores" : False, "Taille des boules" : False, "Version dynamique" : False, "Terminaison" : False, "Obstacles" : False}
    rectangle(0, 0, 800, 600, remplissage="white")
    rectangle(0, 0, 800, 50, remplissage="purple")
    texte(350, 20,"Batailles des boules", ancrage="center")
    
    rectangle(300, 170, 500, 230, remplissage="sky blue")
    texte(300, 170, "Joueur VS IA", taille = 34)
    
    rectangle(300, 350, 500, 410, remplissage="sky blue")
    texte(300, 350, "IA VS IA", taille = 34)
    
    rectangle(300, 50, 500, 110, remplissage="sky blue")
    texte(300, 50, "Sablier", taille = 34)
    
    rectangle(550, 170, 750, 230, remplissage="sky blue")
    texte(550, 170, "Scores", taille = 34)
    
    rectangle(550, 350, 750, 410, remplissage="sky blue")
    texte(550, 350, "Obstacles", taille = 30)
    
    rectangle(300, 470, 500, 580, remplissage="sky blue")
    texte(300, 470, "Taille des", taille = 30)
    texte(335, 520, "boules", taille = 30)
    
    rectangle(50, 170, 270, 230, remplissage="sky blue")
    texte(50, 170, "Terminaison", taille = 27)
    
    rectangle(50, 330, 270, 440, remplissage="sky blue")
    texte(80, 330, "Version", taille = 27)
    texte(60, 380, "dynamique", taille = 27)
    
    rectangle(680, 530, 800, 600, remplissage="purple")
    texte(690, 540, "Suite", taille = 27)
    
    evenement = attente_clic()
    x = evenement[0]
    y = evenement[1]

    while x<680 or y<530:
        if 300<x<500 and 50<y<110:
            if choix["Sablier"] == False:
                choix["Sablier"] = True
                rectangle(300, 50, 500, 110, remplissage="green")
                texte(300, 50, "Sablier", taille = 34)
            else:
                choix["Sablier"] = False
                rectangle(300, 50, 500, 110, remplissage="sky blue")
                texte(300, 50, "Sablier", taille = 34)
                
        elif 550<x<750 and 170<y<230:
            if choix["Scores"] == False:
                choix["Scores"] = True
                rectangle(550, 170, 750, 230, remplissage="green")
                texte(550, 170, "Scores", taille = 34)
            else:
                choix["Scores"] = False
                rectangle(550, 170, 750, 230, remplissage="sky blue")
                texte(550, 170, "Scores", taille = 34)

        elif 550<x<750 and 350<y<410:
            if choix["Obstacles"] == False:
                choix["Obstacles"] = True
                rectangle(550, 350, 750, 410, remplissage="green")
                texte(550, 350, "Obstacles", taille = 30)
            else:
                choix["Obstacles"] = False
                rectangle(550, 350, 750, 410, remplissage="sky blue")
                texte(550, 350, "Obstacles", taille = 30)

        elif 300<x<500 and 470<y<580:
            if choix["Taille des boules"] == False:
                choix["Taille des boules"] = True
                rectangle(300, 470, 500, 580, remplissage="green")
                texte(300, 470, "Taille des", taille = 30)
                texte(335, 520, "boules", taille = 30)
            else:
                choix["Taille des boules"] = False
                rectangle(300, 470, 500, 580, remplissage="sky blue")
                texte(300, 470, "Taille des", taille = 30)
                texte(335, 520, "boules", taille = 30)

        elif 50<x<270 and 170<y<230:
            if choix["Terminaison"] == False:
                choix["Terminaison"] = True
                rectangle(50, 170, 270, 230, remplissage="green")
                texte(50, 170, "Terminaison", taille = 27)
            else:
                choix["Terminaison"] = False
                rectangle(50, 170, 270, 230, remplissage="sky blue")
                texte(50, 170, "Terminaison", taille = 27)

        elif 50<x<270 and 330<y<440:
            if choix["Version dynamique"] == False:
                choix["Version dynamique"] = True
                rectangle(50, 330, 270, 440, remplissage="green")
                texte(80, 330, "Version", taille = 27)
                texte(60, 380, "dynamique", taille = 27)
            else:
                choix["Version dynamique"] = False
                rectangle(50, 330, 270, 440, remplissage="sky blue")
                texte(80, 330, "Version", taille = 27)
                texte(60, 380, "dynamique", taille = 27)
                
        elif 300<x<500 and 170<y<230:
            if choix["JVSIA"] == False:
                choix["JVSIA"] = True
                rectangle(300, 170, 500, 230, remplissage="green")
                texte(300, 170, "Joueur VS IA", taille = 34)
            else:
                choix["JVSIA"] = False
                rectangle(300, 170, 500, 230, remplissage="sky blue")
                texte(300, 170, "Joueur VS IA", taille = 34)
            
        elif 300<x<500 and 350<y<410:
            if choix["IAVSIA"] == False:
                choix["IAVSIA"] = True
                rectangle(300, 350, 500, 410, remplissage="green")
                texte(300, 350, "IA VS IA", taille = 34)
            else:
                choix["IAVSIA"] = False
                rectangle(300, 350, 500, 410, remplissage="sky blue")
                texte(300, 350, "IA VS IA", taille = 34)
        
        
        evenement = attente_clic()
        x = evenement[0]
        y = evenement[1]
    
    return choix


def jeu_profilage():
    fenetre_creee = False  # Indicateur pour suivre si la fenêtre est créée
    try:
        # Création de la fenêtre
        cree_fenetre(800, 600)
        fenetre_creee = True  # La fenêtre est maintenant créée
        print("Fenêtre créée avec succès.")
        
        # Menu et lancement du jeu principal
        choix = menu()
        while choix["JVSIA"] and choix["IAVSIA"]:
            print("Attention! Vous devez choisir entre Joueur VS IA ou IA VS IA, mais pas les deux.")
            choix = menu()
        
        print("Cliquez dans la zone pour créer une boule, dans une boule ennemie pour la diviser.")
        main(choix)  # Lance le jeu principal
    
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    
    finally:
        # Vérifie si la fenêtre a été créée avant de tenter de la fermer
        if fenetre_creee:
            try:
                ferme_fenetre()
                print("Fenêtre fermée avec succès.")
            except Exception as e:
                print(f"Erreur lors de la fermeture de la fenêtre : {e}")
        else:
            print("La fenêtre n'a pas été créée, rien à fermer.")



if __name__ == '__main__':
    import cProfile

    # Lancer le profilage
    cProfile.run('jeu_profilage()', sort='time')

