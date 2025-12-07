# 🔄 Migration V1 → V2

Guide de migration de SteamPy V1 (PyQt5) vers V2 (PyQt6)

## 📋 Résumé des Changements

### Framework UI
- **V1**: PyQt5
- **V2**: PyQt6
- **Impact**: API modernisée, meilleures performances

### Nouveautés V2

| Fonctionnalité | V1 | V2 |
|---------------|----|----|
| Framework | PyQt5 | ✅ PyQt6 |
| Thème Sombre | ❌ | ✅ Oui + Toggle |
| Sauvegarder Liste | ❌ | ✅ Format JSON |
| Charger Liste | .txt seulement | ✅ .txt + .json |
| Sélection Jeux | ❌ | ✅ Checkboxes |
| Recherche Jeux | ❌ | ✅ Barre de recherche |
| Liens Cliquables | ❌ | ✅ Vers Steam Store |
| Images Jeux | ❌ | ✅ Headers officiels |
| Calcul Économies | Basique | ✅ Avancé avec % |
| Menu Bar | ❌ | ✅ Complet |
| Progress Bar | ❌ | ✅ Oui |
| Scrolling | Limité | ✅ Optimisé |

## 🚀 Comment Migrer

### Option 1: Garder vos Listes .txt

Votre fichier `list.txt` de V1 fonctionne directement avec V2!

```bash
# Dans V2
1. Copiez votre list.txt de V1
2. Menu Fichier > Charger .txt
3. Sélectionnez votre fichier
4. Tout fonctionne! 🎉
```

### Option 2: Convertir en Format JSON (Recommandé)

Le format JSON permet de sauvegarder plus d'informations:

```bash
# Dans V2
1. Chargez votre list.txt
2. Menu Fichier > Sauvegarder .json
3. Donnez un nom (ex: ma_collection.json)
4. À l'avenir, chargez le .json directement
```

**Avantages du JSON:**
- Conserve les noms des jeux
- Garde les prix et réductions
- Stocke les liens Steam
- Plus rapide à charger

## 🎨 Nouvelles Fonctionnalités en Détail

### 1. Thèmes Dark/Light

**V1**: Interface claire uniquement
**V2**: Thème sombre par défaut + option claire

```
Menu > Thème > Choisir Sombre/Clair
```

### 2. Gestion de Listes

**V1**: Charger un .txt à chaque fois
**V2**: 
- Sauvegarder plusieurs listes
- Charger instantanément
- Format JSON structuré

**Cas d'usage:**
- `wishlist.json` - Jeux à acheter
- `collection.json` - Jeux possédés
- `soldes.json` - En promotion

### 3. Sélection par Checkboxes

**V1**: Tous les jeux calculés automatiquement
**V2**: Cocher/décocher pour choisir

**Avantages:**
- Comparer différentes combinaisons
- Calculer uniquement les jeux qui vous intéressent
- Simuler des achats

### 4. Recherche de Jeux

**V1**: Éditer manuellement le .txt
**V2**: Barre de recherche intégrée

```
1. Entrez un Steam ID
2. Cliquez "Ajouter"
3. Le jeu apparaît dans la liste
```

### 5. Liens Cliquables

**V1**: Copier/coller l'ID dans Steam
**V2**: Cliquer sur le nom → ouvre Steam Store

### 6. Images des Jeux

**V1**: Texte seulement
**V2**: Headers officiels Steam

**Note:** Les images se chargent automatiquement

## 🔧 Changements Techniques

### Dépendances

**V1:**
```
PyQt5
requests
```

**V2:**
```
PyQt6>=6.6.0
requests>=2.31.0
Pillow>=10.0.0
```

### Installation

**V1:**
```bash
pip install PyQt5 requests
```

**V2:**
```bash
pip install -r requirements.txt
```

### Structure du Code

**V1:**
- Fichier unique: `startapp.py` (197 lignes)
- Fonctions basiques
- UI simple

**V2:**
- Fichier principal: `startapp.py` (545 lignes)
- Architecture orientée objet
- Classes: `SteamPriceApp`, `GameCheckBox`
- Fonctions: 20 fonctions
- Meilleure organisation

### API Steam

**V1:**
- Requêtes basiques
- Pas de limite DLC

**V2:**
- Gestion d'erreurs améliorée
- Limite de 10 DLC (performance)
- Timeouts configurés
- Meilleure gestion des images

## 📊 Comparaison Performance

| Aspect | V1 | V2 |
|--------|----|----|
| Chargement 10 jeux | ~20s | ~15s |
| UI Responsive | Limitée | ✅ Améliorée |
| Mémoire | ~50MB | ~60MB |
| Temps de calcul | Instant | Instant |

## ⚠️ Points d'Attention

### Compatibilité

✅ **Compatible:**
- Fichiers .txt de V1 → V2
- Même format de Steam ID
- Même API Steam

❌ **Non compatible:**
- Fichiers .json de V2 → V1 (V1 ne supporte pas JSON)

### Migration des Scripts

Si vous aviez des scripts qui utilisaient V1:

**V1:**
```python
from PyQt5.QtWidgets import QApplication
```

**V2:**
```python
from PyQt6.QtWidgets import QApplication
```

Principaux changements:
- `exec_()` → `exec()` 
- Enums: `Qt.AlignCenter` → `Qt.AlignmentFlag.AlignCenter`

## 🎯 Recommandations

### Pour les Utilisateurs Basiques
1. Continuez avec vos .txt
2. Testez le thème sombre
3. Profitez des images

### Pour les Utilisateurs Avancés
1. Convertissez en .json
2. Créez plusieurs listes thématiques
3. Utilisez les checkboxes pour comparer
4. Profitez de la recherche

### Pour les Développeurs
1. Consultez CONTRIBUTING.md
2. Code plus structuré pour contribuer
3. Meilleure base pour nouvelles features

## 🆘 Support

**Problèmes de Migration?**
- Discord: https://discord.gg/Z9aKEWsGga
- GitHub Issues: [Créer une issue](https://github.com/stadiag/-SteamPy_V2_PyQt6/issues)
- Email: all.infiny@gmail.com

## 📅 Roadmap Future

Fonctionnalités prévues:
- [ ] Recherche par nom de jeu (pas seulement ID)
- [ ] Historique des prix
- [ ] Notifications de réductions
- [ ] Support multi-devises
- [ ] Export Excel/CSV
- [ ] Comparaison de listes

---

**Merci d'utiliser SteamPy V2!** 🚀

La V2 est une réécriture complète qui conserve la simplicité de V1 tout en ajoutant des fonctionnalités modernes. N'hésitez pas à donner votre avis!
