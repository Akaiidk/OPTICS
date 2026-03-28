# 📊 OPTICS & la Méthode du $\xi$ (Xi)
### Analyse de Clustering hiérarchique et adaptatif

Ce dépôt contient une implémentation Python de l'algorithme **OPTICS** (Ordering Points To Identify the Clustering Structure) avec une extraction de clusters basée sur la **méthode du $\xi$**. 

Contrairement aux méthodes à seuil fixe (comme DBSCAN), cette approche permet de détecter des clusters de densités radicalement différentes en analysant les pentes relatives dans le graphique d'accessibilité.

---

## 🚀 Fonctionnalités
* **Extraction $\xi$-extraction :** Identifie les clusters comme des "vallées" en détectant les points de chute (down-slopes) et de remontée (up-slopes).
* **Lissage par Convolution :** Réduit le bruit local pour éviter la fragmentation des clusters.
* **Support Multi-densité :** Capable de trouver un micro-cluster ultra-dense (ex: Élite Maths/Physique) à côté d'un grand cluster diffus (ex: Humanités).

---

## 📂 Jeux de Données inclus
Le projet inclut deux scénarios de test de 400 lignes chacun :
1. **`Reussite_bac.txt`** : Analyse de la réussite au Bac (Note vs Mention TB) par doublettes de spécialités.
2. **`furry.txt`** : Analyse comportementale de communautés en ligne.
3. **`conso_energie_europe.txt`** : Consommation d'énérgie en Europe.
