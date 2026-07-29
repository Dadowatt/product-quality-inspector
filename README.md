# Contrôle Qualité Automatisé des Produits - Vision par Ordinateur

## Description du projet

Ce projet consiste à développer un micro-service d'intelligence artificielle capable d'analyser automatiquement une image de produit et de retourner un diagnostic de contrôle qualité.

L'objectif est de simuler un système utilisé sur une ligne de production afin d'aider les opérateurs à identifier rapidement l'état d'un produit.

L'API repose sur :

- FastAPI pour l'exposition du service REST ;
- PyTorch pour l'inférence du modèle ;
- timm pour l'utilisation du modèle de vision ;
- MobileNetV3 pour la classification d'image.

---

# Fonctionnalités

L'API permet :

- d'envoyer une image via une requête HTTP ;
- de vérifier automatiquement le format de l'image ;
- de limiter la taille des fichiers entrants ;
- d'effectuer une prédiction avec un modèle de vision ;
- de retourner un résultat JSON structuré.

Exemple de réponse :

```json
{
  "status": "conforme",
  "confidence": 0.861,
  "detected_object": "lens cap"
}
```

---

# Architecture du projet

```
vision-quality-api/

├── app
│   ├── __init__.py
│   ├── main.py
│   ├── model.py
│   └── schemas.py
│
├── tests
│   └── test_image.py
│
├── models_evaluation.md
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

---

# Modèle utilisé

## Modèle principal

`timm/mobilenetv3_small_100.lamb_in1k`

Informations :

- Architecture : MobileNetV3 Small
- Dataset : ImageNet-1k
- Licence : Apache-2.0
- Revision :

```
1824797e7887cbec1990e4adbd6675960a36c589
```

Le modèle a été choisi pour :

- sa faible consommation mémoire ;
- sa rapidité d'inférence ;
- son adaptation aux environnements CPU ;
- sa licence compatible avec un usage commercial.

---

# Installation

## 1. Cloner le projet

```bash
git clone <repository-url>

cd vision-quality-api
```

---

## 2. Créer l'environnement virtuel

```bash
python -m venv .venv
```

Activer l'environnement :

Linux :

```bash
source .venv/bin/activate
```

---

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

# Configuration des variables d'environnement

Créer un fichier :

```bash
touch .env
```

Ajouter :

```env
HF_TOKEN=votre_token_huggingface
```

Le token Hugging Face permet l'accès authentifié aux ressources du Hub.

Le fichier `.env` ne doit jamais être envoyé sur GitHub.

Un fichier `.env.example` est fourni pour montrer la configuration attendue.

---

# Lancer l'application

Démarrer le serveur :

```bash
uvicorn app.main:app --reload
```

L'API sera disponible à :

```
http://127.0.0.1:8000
```

Documentation interactive :

```
http://127.0.0.1:8000/docs
```

---

# Utilisation de l'API

## Endpoint

```
POST /inspect-image
```

## Format attendu

La requête doit contenir :

```
multipart/form-data
```

avec un fichier image :

```
file: image.jpg
```

Formats acceptés :

- JPEG
- PNG

Taille maximale :

```
5 MB
```

---

# Exemple avec Swagger

1. Ouvrir :

```
http://127.0.0.1:8000/docs
```

2. Sélectionner :

```
POST /inspect-image
```

3. Cliquer sur :

```
Try it out
```

4. Envoyer une image.

---

# Exemple de résultat

Réponse :

```json
{
  "status": "conforme",
  "confidence": 0.861,
  "detected_object": "lens cap"
}
```

---

# Sécurité et robustesse

Le service intègre :

- validation du type MIME ;
- limitation de taille des images ;
- gestion des erreurs d'ouverture d'image ;
- chargement unique du modèle en mémoire ;
- séparation entre API et logique IA.

---

# Limites actuelles

Le modèle MobileNetV3 utilisé est un modèle généraliste entraîné sur ImageNet-1k.

Il permet de reconnaître des objets mais n'a pas été entraîné spécifiquement pour détecter :

- rayures ;
- fissures ;
- défauts de fabrication ;
- problèmes de finition.

Pour une utilisation industrielle réelle, une étape de fine-tuning serait nécessaire avec un dataset contenant :

- images de produits conformes ;
- images de produits défectueux.

---

# Tests

Lancer les tests :

```bash
pytest
```

---

# Améliorations futures

Les évolutions possibles :

- entraînement sur un dataset industriel personnalisé ;
- ajout d'un vrai classifieur "conforme/défaut" ;
- ajout d'une base historique des inspections ;
- déploiement Docker ;
- monitoring des performances du modèle.