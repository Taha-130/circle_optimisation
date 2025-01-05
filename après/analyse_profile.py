import pstats
import matplotlib.pyplot as plt

# Charger le fichier de statistiques
stats = pstats.Stats("profile.stats")

# Extraire les données
stats.strip_dirs()  # Nettoyer les chemins des fichiers
stats.sort_stats("ncalls")  # Trier par nombre d'appels

# Limiter les données aux 10 fonctions les plus appelées
functions = []
ncalls = []
totaltime = []

for func, stat in stats.stats.items():
    functions.append(f"{func[2]} ({func[0].split('/')[-1]}:{func[1]})")
    ncalls.append(stat[0])  # Nombre d'appels
    totaltime.append(stat[2])  # Temps total

# Prendre les 10 premières fonctions les plus appelées
top_functions = functions[:10]
top_ncalls = ncalls[:10]
top_totaltime = totaltime[:10]

# Générer le graphique pour le nombre d'appels
plt.figure(figsize=(10, 6))
plt.barh(top_functions, top_ncalls, color="skyblue")
plt.title("Top 10 Fonctions par Nombre d'Appels", fontsize=14)
plt.xlabel("Nombre d'Appels", fontsize=12)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Générer le graphique pour le temps total
plt.figure(figsize=(10, 6))
plt.barh(top_functions, top_totaltime, color="orange")
plt.title("Top 10 Fonctions par Temps Total", fontsize=14)
plt.xlabel("Temps Total (s)", fontsize=12)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
