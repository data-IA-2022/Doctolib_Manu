# Doctolib_Manu

## Table des Matières
- [Contexte et Objectifs](#Contexte)
- [Compétences Ciblées](#compétences-ciblées)
- [Schéma de la Base de Données](#schéma-de-la-base-de-données)
- [Prérequis](#Prérequis)
- [Installation et Configuration](#installation-et-configuration)
- [Lancement des tests unitaite](#lancement-des-tests-unitaites)
- [Aperçu du Projet](#aperçu-du-projet)
- [Versions Futures](#versions-futures)

## Contexte
---
- **Projet en Développement** : Intégration à l'équipe Doctolib pour un nouveau projet ambitieux.
- **Objectif de l'Application** : Expansion de la portée des professionnels de santé et facilitation de la publication d'enquêtes sur la santé des patients consentants.

## Objectifs Principaux
---
Le projet pour **DoctoLib** vise à développer une **application web** qui connecte les professionnels de la santé et les patients. Les aspects clés incluent :
- **Gestion sécurisée des comptes** pour médecins et patients.
- **Système ETL** pour traiter les données à l'international.
- **Analyse avancée de données** (régression, clustering, NLP).
- Utilisation de **Python et Django** pour le développement.
- Création d'un **MVP** avec des graphiques interactifs.
- Réalisation de **tests unitaires** avec une couverture d'au moins 70%.


## Compétences Ciblées
---
1. **Développement en Python et Django**: Utilisation de Python et Django pour le développement de l'application.
2. **Conception de Wireframe**: Création de wireframes pour les pages, conformément aux normes d'accessibilité WCAG.
3. **Gestion de Base de Données**: Emploi de SQLite pour la gestion des données.
4. **Développement d’un système ETL**: Mise en place d'un système ETL adapté aux contextes internationaux.
5. **Analyse de Données et Machine Learning**: Intégration de fonctionnalités d'analyse de données et de modèles de machine learning.
6. **Réalisation de Tests Unitaires**: Tests unitaires avec un taux de couverture d’au moins 70%.

## Schéma de la Base de Données
---
Structure de la base d'enregistrement des rapports :

![image](https://github.com/data-IA-2022/Doctolib_Manu/assets/120089092/90f1bb85-336b-4710-abff-8e82f1f33b22)
![image](https://github.com/data-IA-2022/Doctolib_Manu/assets/120089092/47b2cb33-21f3-45e1-8d8c-dbce6f841227)

Appairage patient médecin :

![image](https://github.com/data-IA-2022/Doctolib_Manu/assets/120089092/13ac6fc0-0c95-4aeb-9c97-65e9036f6ce8)

Associer à un groupe d'utilisateurs :

![image](https://github.com/data-IA-2022/Doctolib_Manu/assets/120089092/362f2c13-efaf-4532-8cd3-b926c3c8b64f)

Geston des droits : 

![image](https://github.com/data-IA-2022/Doctolib_Manu/assets/120089092/f0e86714-98da-4144-b821-165fc18b134d)

Gestion des logs :

![image](https://github.com/data-IA-2022/Doctolib_Manu/assets/120089092/a217587d-9149-4bc3-92ff-e9f2f8b136a0)

## Prérequis
---
- Python 3.11.2
- git 2.9.0

## Installation et Configuration
---

### Étape 1: Clonage du Répertoire
Clonez le dépôt depuis GitHub :

```bash
git clone URL_DU_REPO_GITHUB](https://github.com/data-IA-2022/Doctolib_Manu.git)https://github.com/data-IA-2022/Doctolib_Manu.git`
cd Doctolib_Manu
```

### Étape 2: Configuration de l'Environnement Virtuel
Créez et activez un environnement virtuel :

```bash
python -m venv env
# Sur Windows
env\Scripts\activate
# Sur MacOS/Linux
source env/bin/activate
```

### Étape 3: Installation des Dépendances
Installez les dépendances à partir du fichier requirements.txt :

```bash
pip install -r requirements.txt
```

### Étape 4: Configuration de la Base de Données SQLite
L'application est déjà configurée pour utiliser SQLite. Assurez-vous que les paramètres de la base de données dans settings.py sont corrects.

### Étape 5: Application des Migrations
Créez la structure de la base de données :

```bash
python manage.py migrate
```

### Étape 6: Création d'un Superutilisateur (Optionnel)
Créez un superutilisateur pour accéder à l'interface d'administration :

```bash
python manage.py createsuperuser
```
### Étape 7: Lancement du Serveur de Développement

```bash
python manage.py runserver
```

## Lancement des tests unitaites
---

```bash
python manage.py test -v 2
```

## Aperçu du Projet
---

## Versions Futures
---

- Accroitre la couverture des tests unitaires.

- Dans le formulaire historique, si on est connecté entant que médecin, il reste à implémenter un mécanisme de modification des données.

![image](https://github.com/data-IA-2022/Doctolib_Manu/assets/120089092/9867f4b5-c07c-4c80-9aff-952c7576d213)

  Ce mécanisme peut prendre la forme de formulaires de saisie par le patient (Formulaire d'information).
![image](https://github.com/data-IA-2022/Doctolib_Manu/assets/120089092/012a6b9b-db08-49e2-9232-817a3f1d7e9a)





