# Évaluation des modèles de vision - Contrôle qualité automatisé

## 1. Contexte du projet

L'objectif est de développer un micro-service capable d'analyser automatiquement une image d'un produit et de fournir un diagnostic de contrôle qualité.

Le système doit respecter plusieurs contraintes :

- fonctionnement possible sur une machine locale ;
- temps de réponse rapide ;
- consommation mémoire raisonnable ;
- licence compatible avec un usage commercial ;
- intégration simple dans une API FastAPI.

Deux modèles de classification d'image disponibles sur Hugging Face ont été étudiés.

---

# Modèle candidat 1 : timm/mobilenetv3_small_100.lamb_in1k

## Informations générales

- **Nom Hugging Face :** timm/mobilenetv3_small_100.lamb_in1k
- **Type :** Classification d'image
- **Architecture :** MobileNetV3 Small
- **Bibliothèque :** timm
- **Dataset d'entraînement :** ImageNet-1k
- **Licence :** Apache-2.0

## Caractéristiques techniques

| Critère | Valeur |
|---|---|
| Architecture | MobileNetV3 Small |
| Nombre de paramètres | Environ 2.5 millions |
| Taille du modèle | Faible |
| Taille d'entrée | 224 x 224 pixels |
| Dataset | ImageNet-1k |
| Licence | Apache-2.0 |
| Utilisation CPU | Adaptée |
| Utilisation embarquée | Très adaptée |

## Points positifs

- Modèle léger adapté aux environnements avec peu de ressources.
- Temps d'inférence rapide.
- Licence Apache-2.0 compatible avec un usage commercial.
- Facile à intégrer dans un micro-service FastAPI.
- Convient aux applications nécessitant une faible latence.

## Limites

- Le modèle est entraîné sur ImageNet-1k.
- Il reconnaît des objets généraux mais pas spécifiquement les défauts industriels.
- Une adaptation par fine-tuning serait nécessaire avec un dataset contenant :
  - produits conformes ;
  - produits présentant des défauts.

## Résultat du test

Le modèle a été intégré dans l'API FastAPI et testé avec une image réelle.

Exemple de résultat :

```json
{
  "status": "conforme",
  "confidence": 0.861,
  "detected_object": "lens cap"
}
```

---

# Modèle candidat 2 : google/vit-base-patch16-224

## Informations générales

- **Nom Hugging Face :** google/vit-base-patch16-224
- **Type :** Classification d'image
- **Architecture :** Vision Transformer (ViT)
- **Dataset d'entraînement :** ImageNet-1k
- **Licence :** Apache-2.0

## Caractéristiques techniques

| Critère | Valeur |
|---|---|
| Architecture | Vision Transformer (ViT Base) |
| Nombre de paramètres | Environ 86 millions |
| Taille du modèle | Élevée |
| Taille d'entrée | 224 x 224 pixels |
| Dataset | ImageNet-1k |
| Licence | Apache-2.0 |
| Utilisation CPU | Plus coûteuse |
| Utilisation GPU | Recommandée |

## Points positifs

- Architecture moderne basée sur Transformer.
- Très bonnes performances générales en classification d'image.
- Bonne capacité de représentation visuelle.

## Limites

- Beaucoup plus lourd que MobileNetV3.
- Temps d'inférence plus important sur CPU.
- Consommation mémoire plus élevée.
- Moins adapté à un micro-service local avec des ressources limitées.

---

# Comparaison finale

| Critère | MobileNetV3 Small | Vision Transformer Base |
|---|---|---|
| Architecture | CNN léger | Transformer vision |
| Paramètres | ~2.5M | ~86M |
| Rapidité CPU | Très bonne | Moyenne |
| Mémoire nécessaire | Faible | Élevée |
| Licence | Apache-2.0 | Apache-2.0 |
| Intégration API | Simple | Plus lourde |
| Adapté au matériel limité | Oui | Moins adapté |

---

# Choix final

Le modèle retenu est :

**timm/mobilenetv3_small_100.lamb_in1k**

Ce choix est motivé par :

- sa faible consommation mémoire ;
- sa rapidité d'exécution ;
- sa licence Apache-2.0 autorisant un usage commercial ;
- sa bonne compatibilité avec un micro-service FastAPI local.

Même si Vision Transformer peut obtenir de meilleures performances générales, MobileNetV3 correspond mieux aux contraintes du projet.

Une évolution future consisterait à effectuer un fine-tuning de MobileNetV3 avec un dataset spécifique de contrôle qualité contenant des images de produits conformes et défectueux.

---

# Référence du modèle retenu

- Modèle : timm/mobilenetv3_small_100.lamb_in1k
- Revision : 1824797e7887cbec1990e4adbd6675960a36c589
- Licence : Apache-2.0