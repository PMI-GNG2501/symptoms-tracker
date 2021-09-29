# Suivi des symptomes (Groupe FA2)

## Introduction
Ce projet fait en Python (Avec Django), permet de prendre en note les symptomes de notre cliente atteinte de fibromyalgie, suivre ses traitements et envoyer des rappels. 

## Arborescence du projet
    .
    ├── pages                   # Pages statiques du site (Page d'accueil etc)
    ├── symptoms                # Modèle de symptômes
    ├── symptoms_tracker        # Dossier de configuration du site
    ├── templates               # Gabarit de la page HTML
    ├── users                   # Système de création et de connection de compte
    ├── .gitignore              # Fichier pour ignorer des fichiers de git
    ├── manage.py               # Fichier Django pour effectuer une liste d'action
    ├── README.md  
    └── requirements.txt

## Dépendences Python
- python3
- Django
- django-crispy-forms
- psycopg2
- python-dotenv

## Conventions

1) Toujours ajouter au README.md et requirements.txt les dépendances rajoutées
2) **JAMAIS** mettre des mots de passe dans des fichiers non-couverts par le .gitignore

## Demarrage de l'application
1) Installation de [Python 3](https://www.python.org/downloads/) (Python 3.8 ou + recommandé)
2) Installation de [PIP](https://pip.pypa.io/en/stable/installation/)
3) Création d'une base de donnée PostgresSQL (Ou utilisation d'une base de donnée PostgreSQL existante)
4) Cloner le dépôt Github
5) Ajout de toutes les dépendances avec :
```bash
pip install -r requirements.txt
```

## Deploiement
Le deploiement est automatique dès que quelque chose est envoyé sur la branche "main" sur Github. Celui-ci sera automatiquement deployé sur Heroku.

## Auteurs
- [Arthur Fétiveau](https://github.com/art29)
- [Ayanna Levert-Westmacott](https://github.com/YOURUSERNAME)
- [Ghita Dounia](https://github.com/YOURUSERNAME)
- [Hossein Hajmirbaba](https://github.com/YOURUSERNAME)
- [Jean-Gabriel De Montigny](https://github.com/YOURUSERNAME)
- [Nicholas Turbide](https://github.com/YOURUSERNAME)