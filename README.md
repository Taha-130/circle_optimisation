# Circle War 🟢🔴

## Description

Ce projet est un jeu au tour par tour où le but est d’occuper la plus grande surface coloriée avec sa couleur. Ce jeu permet d'explorer des concepts d'optimisation, de profilage des performances et de mémoire.

---

## Pré-requis

Avant de commencer, vous devez disposer de :

1. **Python** (version 3.10 ou plus récente).
2. Un terminal pour exécuter les commandes.
3. Une bibliothèque graphique (`upemtk`) pour les visuels du jeu.

---

## Installation

### 1. Clonez le dépôt

Clonez le projet depuis le dépôt GitHub :

```bash
git clone https://github.com/votre-utilisateur/projet-circle-war.git
cd projet-circle-war
```

### 2. Créez et activez un environnement virtuel

- **Sur macOS/Linux :**

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **Sur Windows (cmd) :**
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

### 3. Vérifiez que l'environnement virtuel est actif

Une fois activé, `(venv)` doit apparaître au début de la ligne de commande, comme ceci :

```bash
(venv) user@machine:~/Optimisation$
```

### 4. Installez les dépendances

Installez les dépendances nécessaires pour exécuter le projet :

```bash
pip install -r requirements.txt
```

---

## Lancement du Jeu

### 1. Lancer le scénario optimisé

Pour exécuter le jeu optimisé, utilisez la commande suivante :

```bash
python circle_war_apres_profiling_cpu.py
```

### 2. Configuration pour les tests de performance

L'option par défaut est **IA contre IA** avec 10 tours. Cette configuration est utilisée pour analyser les performances et la mémoire.

---

## Tests de Performance

Le projet inclut des outils pour analyser les performances avant et après optimisation.

### 1. Profilage du temps d'exécution avec `cProfile`

Pour analyser le temps d'exécution des fonctions :

```bash
python -m cProfile -o profile.stats circle_war_apres_profiling_memory.py
```

### 2. Profilage de la mémoire avec `memory_profiler`

```bash
python -m memory_profiler circle_war_apres_profiling_memory.py
```

### 3. Comparaison des performances avant et après optimisation

Pour comparer les performances entre la version avant et après optimisation :

- **Avant optimisation** :
  ```bash
  python avant/circle_war_avant_profiling_cpu.py
  ```
- **Après optimisation** :
  ```bash
  python après/circle_war_avant_profiling_cpu.py
  ```

---

## Résolution des Problèmes

### Problème d’installation des dépendances

Si des dépendances manquent, assurez-vous que votre environnement virtuel est actif et exécutez :

```bash
pip install -r requirements.txt
```

### Vérifiez les versions de Python et des packages

- Pour vérifier la version de Python :

  ```bash
  python --version
  ```

- Pour vérifier les packages installés :
  ```bash
  pip list
  ```

---

## Contribution

### Pour contribuer :

1. Créez une branche pour vos modifications :

   ```bash
   git checkout -b nom-de-votre-branche
   ```

2. Effectuez vos modifications, puis ajoutez-les et poussez-les :

   ```bash
   git add .
   git commit -m "Description des modifications"
   git push origin nom-de-votre-branche
   ```

3. Ouvrez une **Pull Request** sur le dépôt GitHub.

---
