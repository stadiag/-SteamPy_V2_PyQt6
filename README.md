# 🎮 SteamPy V2 - PyQt6

Récupérateur automatisé de prix Steam pour liste de jeux (DLC + Games + Prices)

## ✨ Nouveautés de la V2

Cette version V2 reprend toutes les fonctionnalités de la V1 (PyQt5) et ajoute de nombreuses améliorations :

### 🆕 Nouvelles Fonctionnalités

- **🎨 Thème Sombre/Clair** : Interface moderne avec support du thème sombre par défaut
- **💾 Sauvegarde de Listes** : Enregistrez vos listes de jeux au format JSON pour les réutiliser
- **📥 Chargement de Listes** : Rechargez vos listes sauvegardées instantanément
- **☑️ Sélection de Jeux** : Cochez/décochez les jeux pour calculer uniquement ceux qui vous intéressent
- **🔍 Recherche de Jeux** : Ajoutez des jeux à votre liste via une barre de recherche (Steam ID)
- **🔗 Liens Cliquables** : Accédez directement aux pages Steam Store des jeux
- **🖼️ Images de Jeux** : Visualisez les images officielles des jeux directement dans l'application
- **📊 Statistiques Avancées** : Calcul des économies réalisées avec les réductions
- **⚡ Interface Améliorée** : Menus, barre de progression, scrolling fluide

## 📋 Prérequis

```bash
Python >= 3.10
PyQt6 >= 6.6.0
requests >= 2.31.0
Pillow >= 10.0.0
```

## 🚀 Installation

1. Clonez ce dépôt :
```bash
git clone https://github.com/stadiag/-SteamPy_V2_PyQt6.git
cd -SteamPy_V2_PyQt6
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## 💻 Utilisation

Lancez l'application :
```bash
python startapp.py
```

### Méthodes pour ajouter des jeux :

1. **Fichier .txt** : Créez un fichier texte avec un Steam ID par ligne (voir `list.txt` comme exemple)
2. **Recherche manuelle** : Utilisez la barre de recherche pour ajouter des jeux un par un
3. **Fichier .json** : Chargez une liste sauvegardée précédemment

### Exemple de fichier list.txt :

```
32510
32440
438640
920210
311770
```

Chaque ligne contient l'AppID Steam d'un jeu. Vous pouvez trouver l'AppID dans l'URL de la page Steam :
`https://store.steampowered.com/app/APPID/nom-du-jeu`

## 🎯 Fonctionnalités Détaillées

### Prix et Réductions
- Affichage du prix original et du prix avec réduction
- Calcul automatique du pourcentage de réduction
- Support complet des DLC avec leurs prix individuels
- Calcul du total avec et sans réductions

### Interface Utilisateur
- **Menu Fichier** : Charger/Sauvegarder des listes
- **Menu Thème** : Basculer entre thème sombre et clair
- **Menu Aide** : Informations sur l'application
- **Checkboxes** : Sélectionnez uniquement les jeux qui vous intéressent
- **Images** : Visualisez les headers des jeux Steam
- **Liens** : Cliquez sur le nom d'un jeu pour ouvrir sa page Steam

### Gestion des Listes
- Sauvegarde au format JSON avec toutes les informations
- Chargement instantané des listes sauvegardées
- Support des fichiers .txt de la V1 (compatibilité ascendante)

## 📊 Capture d'écran

L'application affiche :
- Liste des jeux avec images et checkboxes
- Prix originaux et réduits
- DLC associés à chaque jeu
- Total des prix sélectionnés
- Économies réalisées

## 🔧 Technologies Utilisées

- **PyQt6** : Framework GUI moderne pour Python
- **Requests** : Récupération des données depuis l'API Steam
- **Pillow** : Traitement et affichage des images
- **Steam API** : API officielle pour récupérer les informations des jeux

## 📝 Notes

- L'application limite le nombre de DLC récupérés à 10 par jeu pour éviter des requêtes excessives
- Un délai peut être nécessaire lors du chargement de nombreux jeux
- Les images sont chargées de manière asynchrone pour ne pas bloquer l'interface
- Le thème sombre est appliqué par défaut

## 🤝 Contribution

Ce projet est entièrement **OPEN-SOURCE**. N'hésitez pas à :
- Fork le projet
- Proposer des améliorations
- Signaler des bugs
- Partager vos listes de jeux !

## 📞 Contact

- **Discord** : [https://discord.gg/Z9aKEWsGga](https://discord.gg/Z9aKEWsGga)
- **E-mail** : all.infiny@gmail.com

## 📜 License

Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🔄 Migration depuis V1

Si vous utilisez déjà la V1 (PyQt5), vous pouvez :
1. Copier votre fichier `list.txt` dans ce dossier
2. Le charger avec le bouton "Charger fichier .txt"
3. Sauvegarder au format JSON pour profiter des nouvelles fonctionnalités

---

⭐ Si ce projet vous plaît, n'hésitez pas à mettre une étoile sur GitHub !
