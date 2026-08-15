#!/bin/bash
# generate_readme.sh
# Génère le fichier README.md du projet UpToConnect à la racine du dépôt.
# Usage : placer ce script à la racine de ton projet Django, puis exécuter :
#   bash generate_readme.sh

cat > README.md << 'EOF'
# UpToConnect

Plateforme e-commerce B2B spécialisée dans le matériel informatique professionnel : sonorisation, tableaux interactifs, visioconférence, réseaux/VoIP, sécurité informatique et accessoires.

![Django](https://img.shields.io/badge/Django-5.x-092E20?logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-en%20d%C3%A9veloppement-yellow)

## Aperçu

UpToConnect est une boutique en ligne développée avec Django, pensée pour les professionnels et les organisations (écoles, entreprises, cliniques, hôtels, administrations) souhaitant s'équiper en matériel technologique. Le site propose un catalogue par catégories, un système de panier et de commande, une gestion des comptes clients, ainsi qu'un back-office d'administration complet.

## Fonctionnalités

- **Catalogue produits** organisé par catégories (Tableau interactif, Visioconférence, Sonorisation, Réseaux / VoIP, Sécurité informatique, Accessoires)
- **Fiches produits détaillées** avec gestion du stock et des ruptures
- **Recherche** de produits avec suggestions en temps réel
- **Panier d'achat** persistant avec gestion des quantités
- **Tunnel de commande (checkout)** en plusieurs étapes avec récapitulatif
- **Comptes utilisateurs** : inscription, connexion, gestion du profil
- **Emails automatiques** : confirmation de commande au client et notification à l'équipe UpToConnect
- **Blog** intégré pour du contenu informatif et SEO
- **Pages institutionnelles** : à propos, contact, mentions légales, politique de confidentialité, retours
- **Back-office Django Admin** pour la gestion des produits, commandes, articles et messages de contact
- **Design responsive**, adapté du mobile à l'écran large, avec identité visuelle en dégradé de marque (violet, bleu, rouge, orange)

## Stack technique

| Composant       | Technologie              |
|-----------------|---------------------------|
| Backend         | Django (Python)            |
| Base de données | SQLite (dev) / PostgreSQL (prod recommandé) |
| Frontend        | HTML5, CSS3 (custom, sans framework), JavaScript vanilla |
| Emails          | Django Email Backend (SMTP) |
| Admin           | Django Admin (interface personnalisée) |

## Structure du projet

```
uptoconnect/
├── manage.py
├── requirements.txt
├── uptoconnect/            # Configuration du projet Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                  # Application principale (catalogue, panier, commandes)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/store/
├── static/                 # Fichiers CSS, JS, images statiques
├── media/                  # Fichiers uploadés (images produits, etc.)
└── templates/               # Templates globaux (base.html, footer, navbar)
```

## Installation

### Prérequis

- Python 3.11 ou supérieur
- pip
- (Optionnel) virtualenv

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/<votre-utilisateur>/uptoconnect.git
cd uptoconnect

# 2. Créer et activer un environnement virtuel
python -m venv venv
source venv/bin/activate      # Sur Windows : venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
# Puis éditer .env avec vos propres valeurs (SECRET_KEY, EMAIL_*, etc.)

# 5. Appliquer les migrations
python manage.py migrate

# 6. Créer un superutilisateur (accès à l'admin)
python manage.py createsuperuser

# 7. Lancer le serveur de développement
python manage.py runserver
```

Le site est ensuite accessible sur `http://127.0.0.1:8000` et l'administration sur `http://127.0.0.1:8000/admin`.

## Configuration des emails

Le projet envoie automatiquement deux emails lors d'une commande validée :
- Une **confirmation de commande** au client
- Une **notification de nouvelle commande** à l'équipe UpToConnect

Configurez les variables suivantes dans votre fichier `.env` :

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-adresse@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-application
DEFAULT_FROM_EMAIL=UpToConnect <contact@uptoconnect.com>
ADMIN_EMAIL=contact@uptoconnect.com
```

## Variables d'environnement

| Variable            | Description                                  |
|---------------------|-----------------------------------------------|
| `SECRET_KEY`        | Clé secrète Django                             |
| `DEBUG`              | `True` en développement, `False` en production |
| `ALLOWED_HOSTS`      | Domaines autorisés en production                |
| `DATABASE_URL`       | URL de connexion à la base de données          |
| `EMAIL_HOST_USER`    | Adresse email d'envoi                          |
| `EMAIL_HOST_PASSWORD`| Mot de passe / mot de passe d'application       |

## Roadmap

- [ ] Intégration d'un moyen de paiement en ligne
- [ ] Espace client avec historique des commandes
- [ ] Système d'avis et de notation produits
- [ ] Export des commandes (CSV / PDF)
- [ ] Internationalisation (FR / EN / AR)

## Contribution

Les contributions sont les bienvenues. Pour proposer un changement :

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/ma-fonctionnalite`)
3. Committez vos changements (`git commit -m 'Ajout de ma fonctionnalité'`)
4. Poussez la branche (`git push origin feature/ma-fonctionnalite`)
5. Ouvrez une Pull Request

## Licence

Ce projet est distribué sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

