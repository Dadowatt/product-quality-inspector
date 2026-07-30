# Vision Quality API

Micro-service de contrôle qualité développé avec **FastAPI** et **Hugging Face Transformers**.

L'API reçoit une image d'un produit, analyse sa surface à l'aide d'un modèle de vision par ordinateur et retourne un diagnostic indiquant si le produit est **conforme** ou présente un **défaut**.

Le projet s'appuie sur le modèle **openai/clip-vit-base-patch32** de Hugging Face et implémente une approche **inspirée de WinCLIP** pour réaliser une détection d'anomalies en **zero-shot**.

---

# Fonctionnalités

- Inspection automatique d'images de produits
- Détection d'anomalies (rayures, fissures, casse, défauts de finition...)
- Approche inspirée de WinCLIP basée sur CLIP
- Analyse par fenêtres glissantes (Sliding Windows)
- Génération automatique de prompts textuels
- Validation des fichiers envoyés
- Réponse JSON structurée
- Documentation interactive avec Swagger

---

# Architecture du projet

```
vision-quality-api/
├── app/
│   ├── config.py
│   ├── main.py
│   ├── model.py
│   ├── schemas.py
│   └── __init__.py
├── tests/
│   ├── test_api.py
│   ├── test_model.py
│   ├── test_images/
│   └── __init__.py
├── models_evaluation.md
├── requirements.txt
├── README.md
└── .env.example
```

---

# Technologies utilisées

- Python 3.12
- FastAPI
- Hugging Face Transformers
- PyTorch
- Pillow
- NumPy
- SciPy
- CLIP ViT-B/32 (Vision Transformer)

---

# Modèle utilisé

Le micro-service utilise le modèle Hugging Face :

**openai/clip-vit-base-patch32**

Ce modèle sert de **backbone de vision** pour extraire les représentations des images et des descriptions textuelles.

Afin de réaliser la détection d'anomalies, le projet implémente une approche **inspirée de WinCLIP**, reposant sur :

- la génération de prompts décrivant des états conformes et défectueux ;
- l'encodage des images et des textes avec CLIP ;
- une analyse par fenêtres glissantes (Sliding Windows) ;
- la construction d'une carte d'anomalies (heatmap) ;
- le calcul d'un score d'anomalie permettant de déterminer si le produit est conforme ou non.

Cette approche permet d'effectuer une détection **zero-shot**, c'est-à-dire sans entraîner un modèle spécifique pour chaque type de produit.

---

# Installation

Cloner le dépôt :

```bash
git clone <url-du-projet>
cd vision-quality-api
```

Créer un environnement virtuel :

```bash
python -m venv .venv
```

Activer l'environnement :

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

# Variables d'environnement

Créer un fichier `.env` à partir de `.env.example` :

```bash
cp .env.example .env
```

Puis renseigner :

```env
HF_TOKEN=votre_token_huggingface
MODEL_NAME=openai/clip-vit-base-patch32
ANOMALY_THRESHOLD=0.75
```

### Description

- **HF_TOKEN** : jeton Hugging Face (optionnel pour les modèles publics, recommandé afin d'éviter les limitations de téléchargement).
- **MODEL_NAME** : modèle CLIP utilisé.
- **ANOMALY_THRESHOLD** : seuil de décision entre un produit conforme et un produit défectueux.

---

# Lancer l'API

```bash
uvicorn app.main:app --reload
```

L'API est disponible sur :

```
http://127.0.0.1:8000
```

Documentation Swagger :

```
http://127.0.0.1:8000/docs
```

---

# Endpoint

## POST /inspect-image

Analyse une image de produit et retourne un diagnostic.

### Paramètres

| Nom | Type | Description |
|------|------|-------------|
| image | File | Image du produit |
| category | String | Catégorie du produit (ex. : metal_nut, bottle, screw...) |

---

# Exemple avec curl

```bash
curl -X POST "http://127.0.0.1:8000/inspect-image" \
-F "image=@tests/test_images/piece_test.jpg" \
-F "category=metal_nut"
```

---

# Exemple de réponse

```json
{
  "status": "defaut",
  "confidence": 0.8,
  "anomaly_score": 0.8
}
```

---

# Pipeline de traitement

Le traitement d'une image suit les étapes suivantes :

1. Réception de l'image par FastAPI.
2. Validation du type et de la taille du fichier.
3. Ouverture de l'image.
4. Prétraitement avec le **CLIPProcessor**.
5. Génération des prompts textuels.
6. Découpage de l'image en fenêtres glissantes.
7. Extraction des caractéristiques visuelles avec **CLIP**.
8. Comparaison entre les représentations des images et des prompts.
9. Construction d'une heatmap d'anomalies.
10. Calcul d'un score d'anomalie.
11. Retour du diagnostic au format JSON.

---

# Tests

Tester directement le modèle :

```bash
python -m tests.test_model
```

Tester l'API :

```bash
python -m tests.test_api
```

Ou avec `curl` :

```bash
curl -X POST "http://127.0.0.1:8000/inspect-image" \
-F "image=@tests/test_images/piece_test.jpg" \
-F "category=metal_nut"
```

---

# Sécurité

Le micro-service intègre plusieurs mécanismes de protection :

- validation du type MIME des fichiers ;
- limitation de la taille des images (5 Mo maximum) ;
- gestion des images invalides ou corrompues ;
- gestion des exceptions lors de l'inférence ;
- configuration via des variables d'environnement.

---

# Auteur

**Dado Watt**

Projet réalisé dans le cadre d'un atelier de développement d'un micro-service d'intelligence artificielle avec **FastAPI** et **Hugging Face Transformers**.