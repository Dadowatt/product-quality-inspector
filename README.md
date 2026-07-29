# Vision Quality API

Micro-service de contrôle qualité développé avec **FastAPI** et **Hugging Face Transformers**.

L'API reçoit une image d'un produit, analyse sa surface à l'aide d'un modèle de vision par ordinateur et retourne un diagnostic indiquant si le produit est **conforme** ou présente un **défaut**.

---

# Fonctionnalités

- Inspection automatique d'images de produits
- Détection d'anomalies (rayures, fissures, casse, défauts de finition...)
- Modèle téléchargé automatiquement depuis Hugging Face au premier démarrage
- Validation des fichiers envoyés
- Réponse JSON structurée
- Documentation interactive avec Swagger

---

# Architecture du projet

```
vision-quality-api/
├── app/
│   ├── main.py
│   ├── model.py
│   ├── schemas.py
│   └── __init__.py
├── tests/
│   ├── test_model.py
│   ├── test_image.py
│   └── __init__.py
├── models_evaluation.md
├── requirements.txt
├── README.md
└── .env
```

---

# Technologies utilisées

- Python 3.12
- FastAPI
- Hugging Face Transformers
- CLIP ViT-B/32
- WinCLIP Zero-Shot
- Pillow
- PyTorch

---

# Modèle utilisé

Le projet utilise le modèle :

**rrs-2002/WinCLIP Zero-Shot Defect Detection**

basé sur :

**openai/clip-vit-base-patch32**

Le micro-service implémente l'approche **WinCLIP (Zero-Shot Defect Detection)** en s'appuyant sur le modèle **openai/clip-vit-base-patch32** disponible sur Hugging Face.

Cette approche permet de détecter des anomalies visuelles sur différentes catégories de produits sans entraînement spécifique.

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

Linux / macOS

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

# Variables d'environnement

Créer un fichier `.env` à la racine du projet :

```env
HF_TOKEN=votre_token_huggingface
MODEL_NAME=openai/clip-vit-base-patch32
ANOMALY_THRESHOLD=0.75
```

Le `HF_TOKEN` est recommandé afin d'éviter les limitations de téléchargement depuis Hugging Face.

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

Analyse une image et retourne un diagnostic.

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
  "confidence": 0.763,
  "anomaly_score": 0.763
}
```

---

# Tests

Tester directement le modèle :

```bash
python -m tests.test_model
```

Tester l'API :

```bash
curl -X POST "http://127.0.0.1:8000/inspect-image" \
-F "image=@tests/test_images/piece_test.jpg" \
-F "category=metal_nut"
```

---

# Sécurité

Le micro-service intègre plusieurs mécanismes de protection :

- validation du type de fichier ;
- limitation de la taille des images ;
- gestion des images invalides ou corrompues ;
- gestion des erreurs d'inférence ;
- configuration via variables d'environnement.

---

# Auteur
**Dado Watt**

Projet réalisé dans le cadre d'un atelier de développement d'un micro-service d'intelligence artificielle avec FastAPI et Hugging Face.