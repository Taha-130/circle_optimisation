Bonjour, Bonsoir, Voici une explication de notre programme concernant:
— les choix ;
— l’organisation du programme ;
— les choix techniques ; 
— et les problèmes rencontrés.

— Les choix 

Pour cette partie nous avons choisi de laisser l'utilisateur lancer le programme et répondre sur le Shell aux questions, pour les paramètres du jeu, par lui même, sauf pour le choix des variantes.

— L’organisation du programme et les choix techniques

Le programme fonctionne donc avec le choix des variantes au début avec un menu, la partie principale plutôt dans la fonction main, mais qui est aussi dépendante de la fonction tours (pour les joueurs ou de l'IA) ainsi que quelques fonctions plus ou moins mineures.

Dans le programme principal, après la prise des préférences, la création de la fenêtre et l'initialisation de variables. La boucle dans laquelle les utilisateurs placent leurs boules commence. Les utilisateurs jouent un tour sur deux, avec un compteur qui baisse petit à petit. 

Time est utilisé pour définir un temps max pour pouvoir tester plus tard si le temps a été dépassé par l'utilisateur. Nous avons donc décidé que le tour ne se passe pas automatiquement lorsqu'un joueur met trop de temps, car cela pourrait impacter l'autre joueur. Alors quand le premier cliquera, il verra que son tour a été passé, puis le deuxième pourra jouer.

En ce qui concerne le placement de points, nous avons décidé que les bords du jeu ne peuvent pas être dépassés, donc on ne peut pas voir un cercle coupé par les limites et le cadre en haut ne doit pas être gêné non plus. Si il n'y a pas de problème, une boule est placée.

Chaque boule est sauvegardée puisque c'est ce qu'il faut pour tester si le point cliqué est valide, on garde le maximum d'informations dans cette liste de liste, en préparation pour les futurs projets. 

Quand la boucle est finie, et donc que les joueurs ont finit de placer leurs boules, on calcule la surface de l'un et de l'autre, puis on fait un calcul et affichage du gagnant.
À la fin, en cliquant une dernière fois, le jeu se termine.


- L'IA et la sauvegarde des scores

Ce sont les deux amélioration que nous avons choisis pour notre jeu, il est possible d'avoir une IA ou de voir deux IA se battre entre elles. Les choix de l'IA sont aléatoires sauf pour quelques exceptions qui permettent de donner un ressenti assez proche d'un vrai joueur. 
D'abord pour le placement de boules, l'IA va faire son choix aléatoirement MAIS va prioriser les emplacements totalement libre, puis placer des boules au dessus de celles alliés, ou diviser les boules ennemies.

Si jamais elle est en train de gagner, il y a des chances qu'elle divise une boules ennemie car ça peut possiblement laisser une chance au joueur de gagner et faire une remontée dans le score.

Enfin si le mode de jeu était joueur contre IA, à la fin le score du joueur va être sauvegardé dans le fichier classement.txt, et le programme va afficher le classement des 5 meilleurs (même si il y a plus que cinq scores sauvegardés car la liste créée dans le programme et triée puis coupée).

— Les problèmes rencontrés

Il y a eu des problèmes mineurs comme le sablier qui se lançait en dehors de la boucle, ce qui causait le programme de juger tout le temps que les joueurs étaient trop lents, ou encore des problèmes que nous avions pas totalement compris mais réussi à éviter.

Toutefois nous avons eu deux défis difficiles dont le premier est celui de la division d’une boule ennemie, elle se produit mais n’efface pas le cercle précédent nous avons donc décidé d’introduire une boule blanche par dessus afin de masquer la boule derrière non divisée.

Nous avons pas pu régler à temps le deuxième défi qui était la variable "Version dynamique". En effet elle nous a crée trop de bugs alors nous avons effacé totalement la variable du programme et mis un message expliquant qu'il n'était pas possible de l'avoir si on veut la choisir.

Nous voudrions régler ces problème au plus vite même si nous ne serons plus noté dessus afin d'avoir un projet fini mais ça n'a pas été possible pour ce troisième rendu.


Merci pour votre attention.
Cordialement,
Temle Bogdan et Sefoudine Taha