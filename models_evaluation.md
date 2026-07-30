# Évaluation des modèles de vision

## Objectif

Dans le cadre de ce projet, deux modèles de vision par ordinateur issus du Hub Hugging Face ont été étudiés afin de sélectionner la solution la plus adaptée à un micro-service de contrôle qualité capable de détecter automatiquement des défauts visuels sur des produits manufacturés.

Les critères de comparaison sont :
- performances pour la détection de défauts ;
- taille et facilité de déploiement ;
- licence d'utilisation ;
- adéquation avec le contexte du projet.

---


## Modèle 1 : Keyven/AnomalyDetection-MVTech-Metal

**Type :** Détection d'anomalies OpenVINO

**Licence :** Apache 2.0

**Taille :** 377MB

### Avantages

- Modèle léger optimisé pour OpenVINO.
- Très rapide en inférence sur CPU.
- Téléchargement simple depuis Hugging Face.

### Inconvénients

- Entraîné uniquement sur la catégorie **Metal** du jeu de données MVTec AD.
- Les résultats deviennent peu fiables sur d'autres types de produits.
- Peu adapté à un atelier produisant des objets variés.

### Conclusion

Ce modèle offre de bonnes performances pour des pièces métalliques, mais son domaine d'application est trop restreint pour répondre au contexte général du projet.

---

## Modèle 2 : Approche WinCLIP basée sur CLIP ViT-B/32

**Backbone utilisé :** openai/clip-vit-base-patch32

**Méthode :** Implémentation inspirée de WinCLIP (Zero-Shot Defect Detection)

**Licence :** MIT

**Taille :** ~600 Mo (poids du modèle CLIP ViT-B/32)

### Avantages

- Détection de défauts en **zero-shot** (sans entraînement spécifique).
- Peut être utilisé sur différentes catégories de produits.
- Détecte des anomalies telles que :
  - rayures ;
  - fissures ;
  - casse ;
  - défauts de finition.
- Compatible avec Hugging Face Transformers.

### Inconvénients

- Plus lourd qu'un modèle OpenVINO.
- Temps d'inférence légèrement supérieur sur CPU.

### Conclusion

L'approche WinCLIP repose sur le modèle CLIP ViT-B/32 pour effectuer une détection d'anomalies en zero-shot. Dans ce projet, nous avons implémenté cette approche en utilisant le backbone `openai/clip-vit-base-patch32` et les bibliothèques Hugging Face Transformers. Cette solution permet d'inspecter plusieurs catégories de produits sans entraîner un modèle spécifique pour chacune d'elles.

---

# Comparaison des modèles

| Critère  | Keyven / AnomalyDetection-MVTech-Metal | WinCLIP (OpenAI CLIP ViT-B/32) |
|:---------|:---------------------------------------|:-------------------------------|
| **Licence**                   |  Apache 2.0    ✅ | MIT ✅                         |
| **Architecture**              | OpenVINO          |CLIP Vision Transformer         |
| **Type de détection**         |Anomaly Detection  |Zero-shot Anomaly Detection     |
| **Entraînement requis**       | Oui               |  Non                           |    
| **Détection multi-produits**  | ❌ Limitée        | ✅ Oui                         |
| **Détection Zero-shot**       | ❌ Non            | ✅ Oui                         |
| **Optimisé CPU**              | ✅ Excellent      | ✅ Bon                         |  
| **Flexibilité**               | Faible            | Élevée                         |
| **Adapté au contexte de l'atelier** | Moyen       |   ⭐Excellent                  |

---

# Modèle retenu

L'approche WinCLIP, implémentée à partir du backbone `openai/clip-vit-base-patch32`, a été retenue pour le développement du micro-service.

### Raisons du choix

- Licence **MIT** compatible avec un usage commercial.
- Détection **Zero-shot** sans phase d'entraînement.
- Peut inspecter plusieurs catégories de produits.
- Détection de défauts variés (rayures, fissures, casse, trous, mauvaise finition).
- Compatible avec une intégration FastAPI.
- Basé sur **OpenAI CLIP (ViT-B/32)**, largement utilisé en vision par ordinateur.

Ce modèle répond le mieux au contexte du projet, où les produits inspectés peuvent être différents d'une ligne de production à une autre.