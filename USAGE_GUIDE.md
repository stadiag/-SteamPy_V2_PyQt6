# 📖 Guide d'Utilisation - SteamPy V2

## 🚀 Démarrage Rapide

### 1. Installation
```bash
# Cloner le dépôt
git clone https://github.com/stadiag/-SteamPy_V2_PyQt6.git
cd -SteamPy_V2_PyQt6

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Lancement
```bash
python startapp.py
```

## 🎯 Fonctionnalités Principales

### 📂 Charger des Jeux

#### Méthode 1: Fichier .txt
1. Créez un fichier texte avec un Steam ID par ligne
2. Cliquez sur "📂 Charger fichier .txt"
3. Sélectionnez votre fichier
4. Les jeux se chargent automatiquement

**Exemple de fichier list.txt:**
```
32510
32440
438640
```

#### Méthode 2: Recherche Manuelle
1. Entrez un Steam ID dans la barre de recherche
2. Cliquez sur "➕ Ajouter"
3. Le jeu est ajouté à votre liste

**Comment trouver un Steam ID?**
- Allez sur la page Steam du jeu
- L'URL ressemble à: `https://store.steampowered.com/app/STEAMID/nom-du-jeu`
- Le STEAMID est le nombre dans l'URL

#### Méthode 3: Charger une Liste Sauvegardée
1. Cliquez sur "📥 Charger liste .json"
2. Sélectionnez votre fichier .json
3. Votre liste est restaurée

### 💾 Sauvegarder une Liste

1. Ajoutez des jeux à votre liste
2. Cliquez sur "💾 Sauvegarder liste .json"
3. Choisissez l'emplacement et le nom
4. Votre liste est sauvegardée avec tous les détails

### 💰 Calculer les Prix

1. Cochez les jeux que vous voulez inclure dans le calcul
2. Décochez ceux que vous ne voulez pas
3. Cliquez sur "💰 Calculer les prix"
4. Les résultats s'affichent en bas avec:
   - Prix original de chaque jeu
   - Prix avec réduction
   - DLC et leurs prix
   - Total et économies réalisées

### 🎨 Changer le Thème

**Menu Thème:**
- **Thème Sombre** (par défaut): Interface sombre moderne
- **Thème Clair**: Interface classique claire

Accédez au menu via: `Thème > Thème Sombre/Clair`

## 💡 Astuces et Conseils

### Optimisation
- **Limiter le nombre de jeux**: Le chargement de nombreux jeux peut prendre du temps
- **DLC limités**: L'application charge max 10 DLC par jeu pour éviter les délais
- **Sauvegardez régulièrement**: Créez des listes thématiques (wishlist, collection, etc.)

### Navigation
- **Cliquez sur le nom d'un jeu**: Ouvre sa page Steam dans votre navigateur
- **Images**: Les images des jeux se chargent automatiquement
- **Barre de progression**: S'affiche pendant les opérations longues

### Organisation
Créez plusieurs listes pour différents usages:
- `wishlist.json` - Jeux à acheter
- `collection.json` - Jeux possédés
- `soldes.json` - Jeux en promotion
- `multijoueur.json` - Jeux multijoueur

## 🐛 Résolution de Problèmes

### Le jeu ne se charge pas
- Vérifiez que le Steam ID est correct
- Assurez-vous d'avoir une connexion internet
- Certains jeux peuvent être indisponibles ou retirés du Store

### Images ne s'affichent pas
- Vérifiez votre connexion internet
- Les images peuvent prendre quelques secondes à charger
- Certains jeux n'ont pas d'images disponibles

### L'application est lente
- Réduisez le nombre de jeux chargés simultanément
- Fermez et relancez l'application
- Vérifiez que vous avez suffisamment de mémoire

## 📊 Format des Fichiers

### Fichier .txt (simple)
```
32510
32440
438640
920210
```
Un Steam ID par ligne, rien d'autre.

### Fichier .json (complet)
```json
{
  "version": "2.0",
  "games": [
    {
      "title": "World of Goo",
      "appid": 32510,
      "final": 9.99,
      "initial": 14.99,
      "discount_percent": 33,
      "store_url": "https://store.steampowered.com/app/32510",
      "header_image": "https://...",
      "dlcs": []
    }
  ]
}
```

## 🔗 Liens Utiles

- **Discord**: https://discord.gg/Z9aKEWsGga
- **GitHub**: https://github.com/stadiag/-SteamPy_V2_PyQt6
- **Steam Store**: https://store.steampowered.com
- **SteamDB** (pour trouver des IDs): https://steamdb.info

## ❓ Questions Fréquentes

**Q: Comment trouver le Steam ID d'un jeu?**
R: Visitez la page Steam du jeu, l'ID est dans l'URL après `/app/`

**Q: Pourquoi certains prix sont à 0€?**
R: Le jeu est gratuit ou n'a pas de prix public (beta, retiré du store, etc.)

**Q: Les DLC sont-ils tous affichés?**
R: Non, maximum 10 DLC par jeu pour optimiser les performances

**Q: Puis-je utiliser mes listes de la V1?**
R: Oui! Chargez votre fichier .txt de V1, puis sauvegardez-le en .json

**Q: L'application fonctionne-t-elle hors ligne?**
R: Non, une connexion internet est nécessaire pour récupérer les prix Steam

**Q: Les prix sont-ils en temps réel?**
R: Oui, les prix sont récupérés en temps réel via l'API Steam officielle

## 📝 Notes Importantes

- **Limites de l'API Steam**: Ne pas faire trop de requêtes rapidement
- **Prix régionaux**: Les prix affichés sont pour la région française (EUR)
- **Réductions temporaires**: Les promotions Steam changent régulièrement
- **Open Source**: N'hésitez pas à contribuer au projet!

---

💝 Merci d'utiliser SteamPy V2! N'hésitez pas à partager vos retours.
