# 🤝 Guide de Contribution

Merci de votre intérêt pour contribuer à SteamPy V2! 

## 🌟 Comment Contribuer

### Signaler un Bug
1. Vérifiez que le bug n'a pas déjà été signalé dans les [Issues](https://github.com/stadiag/-SteamPy_V2_PyQt6/issues)
2. Créez une nouvelle issue avec:
   - Description claire du problème
   - Étapes pour reproduire
   - Comportement attendu vs comportement actuel
   - Captures d'écran si pertinent
   - Votre environnement (OS, version Python)

### Proposer une Fonctionnalité
1. Ouvrez une issue pour discuter de la fonctionnalité
2. Expliquez pourquoi elle serait utile
3. Proposez une implémentation si possible

### Soumettre du Code

#### Prérequis
- Python >= 3.10
- PyQt6
- Connaissance de base de Git

#### Étapes
1. **Fork** le projet
2. **Clone** votre fork
   ```bash
   git clone https://github.com/VOTRE-USERNAME/-SteamPy_V2_PyQt6.git
   ```
3. **Créer une branche** pour votre fonctionnalité
   ```bash
   git checkout -b feature/ma-fonctionnalite
   ```
4. **Installer** les dépendances
   ```bash
   pip install -r requirements.txt
   ```
5. **Développer** votre fonctionnalité
6. **Tester** vos modifications
7. **Commit** vos changements
   ```bash
   git commit -m "Ajout de [fonctionnalité]"
   ```
8. **Push** vers votre fork
   ```bash
   git push origin feature/ma-fonctionnalite
   ```
9. **Créer une Pull Request** sur le dépôt principal

## 📝 Standards de Code

### Style Python
- Suivre PEP 8
- Utiliser des noms de variables descriptifs
- Commenter le code complexe
- Ajouter des docstrings pour les fonctions

### Exemple
```python
def get_steam_price(appid: int, country: str = 'fr') -> dict:
    """
    Récupère le prix d'un jeu Steam.
    
    Args:
        appid: L'identifiant Steam du jeu
        country: Code pays (défaut: 'fr')
    
    Returns:
        dict: Informations du jeu avec les prix
    """
    # Implémentation...
```

### Commits
- Messages clairs et descriptifs
- En français ou anglais
- Format: `[Type] Description courte`
- Types: Feature, Fix, Docs, Style, Refactor

Exemples:
```
[Feature] Ajout de la recherche par nom de jeu
[Fix] Correction du calcul des réductions
[Docs] Mise à jour du README
```

## 🎨 Suggestions de Contributions

### Fonctionnalités Faciles
- [ ] Ajouter plus de thèmes (dark blue, etc.)
- [ ] Améliorer les messages d'erreur
- [ ] Ajouter des raccourcis clavier
- [ ] Traduction en anglais

### Fonctionnalités Intermédiaires
- [ ] Recherche par nom de jeu (pas seulement ID)
- [ ] Export en CSV ou Excel
- [ ] Graphiques de prix dans le temps
- [ ] Filtres avancés (prix, genre, etc.)

### Fonctionnalités Avancées
- [ ] Threading pour améliorer les performances
- [ ] Cache local des données
- [ ] Notifications de réductions
- [ ] Support multi-devises

## 🐛 Tests

Avant de soumettre:
1. Testez votre code localement
2. Vérifiez qu'il n'y a pas de régression
3. Testez sur différents OS si possible
4. Vérifiez les imports et dépendances

## 📖 Documentation

Si vous ajoutez une fonctionnalité:
1. Mettez à jour le README.md
2. Ajoutez des exemples si nécessaire
3. Mettez à jour USAGE_GUIDE.md si pertinent
4. Documentez le code avec des docstrings

## 🔒 Sécurité

Si vous trouvez une vulnérabilité:
- **NE PAS** l'exposer publiquement
- Contactez directement: all.infiny@gmail.com
- Décrivez le problème en détail

## 💬 Questions?

- Discord: https://discord.gg/Z9aKEWsGga
- Email: all.infiny@gmail.com
- Issues GitHub: Pour les discussions publiques

## 📜 License

En contribuant, vous acceptez que vos contributions soient sous la même licence que le projet (voir LICENSE).

---

Merci pour vos contributions! 🙏
