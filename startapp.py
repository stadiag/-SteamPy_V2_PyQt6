import sys
import json
import requests
from io import BytesIO
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFileDialog, QTextEdit, QMessageBox, QLineEdit, QCheckBox,
    QScrollArea, QGroupBox, QProgressBar, QMenuBar, QMenu, QDialog, QDialogButtonBox
)
from PyQt6.QtGui import QFont, QPixmap, QAction
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PIL import Image

# Fonction pour récupérer le prix d'un jeu + ses DLC via l'API Steam
def get_steam_price_with_dlc(appid, country='fr', currency='eur'):
    """
    Récupère les informations de prix pour un jeu Steam et ses DLC
    
    Args:
        appid: L'identifiant Steam du jeu
        country: Code pays (par défaut 'fr')
        currency: Code devise (par défaut 'eur')
    
    Returns:
        dict: Informations du jeu et de ses DLC avec les prix
    """
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc={country}&l=fr"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if not data[str(appid)]["success"]:
            print(f"[DEBUG] AppID {appid} échec d'accès API")
            return None

        info = data[str(appid)]["data"]
        name = info.get("name", f"Unknown Game {appid}")
        print(f"[DEBUG] Récupération du jeu : {name} (AppID {appid})")

        game_price = {
            "title": name,
            "appid": appid,
            "final": 0,
            "initial": 0,
            "discount_percent": 0,
            "dlcs": [],
            "store_url": f"https://store.steampowered.com/app/{appid}",
            "header_image": info.get("header_image", "")
        }

        # Prix du jeu de base
        if "price_overview" in info:
            p = info["price_overview"]
            game_price["final"] = p["final"] / 100
            game_price["initial"] = p["initial"] / 100
            game_price["discount_percent"] = p["discount_percent"]
        else:
            print(f"[DEBUG] Aucun prix trouvé pour le jeu {name}")

        # Récupération des DLC
        if "dlc" in info:
            dlc_ids = info["dlc"]
            print(f"[DEBUG] {len(dlc_ids)} DLC(s) trouvé(s) pour {name}")
            for dlc_id in dlc_ids[:10]:  # Limiter à 10 DLC pour éviter trop de requêtes
                dlc_url = f"https://store.steampowered.com/api/appdetails?appids={dlc_id}&cc={country}&l=fr"
                dlc_resp = requests.get(dlc_url, timeout=10).json()
                if dlc_resp.get(str(dlc_id), {}).get("success"):
                    dlc_data = dlc_resp[str(dlc_id)]["data"]
                    if "price_overview" in dlc_data:
                        d = dlc_data["price_overview"]
                        dlc_info = {
                            "title": dlc_data["name"],
                            "appid": dlc_id,
                            "final": d["final"] / 100,
                            "initial": d["initial"] / 100,
                            "discount_percent": d["discount_percent"],
                            "store_url": f"https://store.steampowered.com/app/{dlc_id}"
                        }
                        game_price["dlcs"].append(dlc_info)
                        print(f"[DEBUG] DLC ajouté : {dlc_info['title']}")
                    else:
                        print(f"[DEBUG] DLC {dlc_id} sans prix (probablement retiré)")
        else:
            print(f"[DEBUG] Aucun DLC pour {name}")

        return game_price
    except Exception as e:
        print(f"[ERROR] Exception pour AppID {appid} : {e}")
        return {"title": f"Erreur {appid}", "error": str(e), "appid": appid}


def download_image(url):
    """Télécharge une image depuis une URL et retourne un QPixmap"""
    try:
        response = requests.get(url, timeout=10)
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB")
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        pixmap = QPixmap()
        pixmap.loadFromData(img_bytes.getvalue())
        return pixmap
    except Exception as e:
        print(f"[ERROR] Erreur lors du téléchargement de l'image : {e}")
        return None


class GameCheckBox(QWidget):
    """Widget personnalisé pour afficher un jeu avec checkbox et image"""
    
    def __init__(self, game_info, parent=None):
        super().__init__(parent)
        self.game_info = game_info
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(True)
        
        layout = QHBoxLayout()
        layout.addWidget(self.checkbox)
        
        # Label avec le nom du jeu (cliquable)
        self.name_label = QLabel(f"<a href='{game_info['store_url']}'>{game_info['title']}</a>")
        self.name_label.setOpenExternalLinks(True)
        self.name_label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(self.name_label)
        
        # Image du jeu (si disponible)
        if game_info.get('header_image'):
            self.image_label = QLabel()
            self.image_label.setText("Chargement...")
            layout.addWidget(self.image_label)
            # Charger l'image de manière asynchrone
            self.load_image_async()
        
        layout.addStretch()
        self.setLayout(layout)
    
    def load_image_async(self):
        """Charge l'image de manière asynchrone"""
        try:
            pixmap = download_image(self.game_info['header_image'])
            if pixmap:
                scaled_pixmap = pixmap.scaled(184, 69, Qt.AspectRatioMode.KeepAspectRatio)
                self.image_label.setPixmap(scaled_pixmap)
            else:
                self.image_label.setText("Image non disponible")
        except:
            self.image_label.setText("Erreur")
    
    def is_checked(self):
        return self.checkbox.isChecked()


class SteamPriceApp(QMainWindow):
    """Application principale pour vérifier les prix Steam"""
    
    def __init__(self):
        super().__init__()
        self.games_data = []
        self.game_widgets = []
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("Steam Price Checker V2 - PyQt6")
        self.setMinimumSize(1000, 700)
        
        # Créer la barre de menu
        self.create_menu_bar()
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Titre
        title = QLabel("🎮 Vérificateur de Prix Steam V2")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Barre de recherche
        search_layout = QHBoxLayout()
        search_label = QLabel("Ajouter un jeu (Steam ID):")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Entrez l'ID Steam du jeu...")
        self.add_game_button = QPushButton("➕ Ajouter")
        self.add_game_button.clicked.connect(self.add_game_by_id)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.add_game_button)
        main_layout.addLayout(search_layout)
        
        # Boutons de contrôle
        button_layout = QHBoxLayout()
        self.load_button = QPushButton("📂 Charger fichier .txt")
        self.load_button.clicked.connect(self.load_file)
        
        self.load_json_button = QPushButton("📥 Charger liste .json")
        self.load_json_button.clicked.connect(self.load_json)
        
        self.save_json_button = QPushButton("💾 Sauvegarder liste .json")
        self.save_json_button.clicked.connect(self.save_json)
        
        self.calculate_button = QPushButton("💰 Calculer les prix")
        self.calculate_button.clicked.connect(self.calculate_selected)
        
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.load_json_button)
        button_layout.addWidget(self.save_json_button)
        button_layout.addWidget(self.calculate_button)
        main_layout.addLayout(button_layout)
        
        # Zone de défilement pour les jeux
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.games_container = QWidget()
        self.games_layout = QVBoxLayout(self.games_container)
        scroll_area.setWidget(self.games_container)
        main_layout.addWidget(scroll_area)
        
        # Zone de résultats
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setMaximumHeight(200)
        main_layout.addWidget(self.result_area)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
    
    def create_menu_bar(self):
        """Crée la barre de menu"""
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu("Fichier")
        
        load_action = QAction("Charger .txt", self)
        load_action.triggered.connect(self.load_file)
        file_menu.addAction(load_action)
        
        load_json_action = QAction("Charger .json", self)
        load_json_action.triggered.connect(self.load_json)
        file_menu.addAction(load_json_action)
        
        save_json_action = QAction("Sauvegarder .json", self)
        save_json_action.triggered.connect(self.save_json)
        file_menu.addAction(save_json_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("Quitter", self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Menu Thème
        theme_menu = menubar.addMenu("Thème")
        
        dark_theme_action = QAction("Thème Sombre", self)
        dark_theme_action.triggered.connect(self.apply_dark_theme)
        theme_menu.addAction(dark_theme_action)
        
        light_theme_action = QAction("Thème Clair", self)
        light_theme_action.triggered.connect(self.apply_light_theme)
        theme_menu.addAction(light_theme_action)
        
        # Menu Aide
        help_menu = menubar.addMenu("Aide")
        
        about_action = QAction("À propos", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def apply_theme(self):
        """Applique le thème par défaut (sombre)"""
        self.apply_dark_theme()
    
    def apply_dark_theme(self):
        """Applique un thème sombre"""
        dark_stylesheet = """
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
            QPushButton:pressed {
                background-color: #0d5080;
            }
            QLineEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 5px;
                border-radius: 3px;
            }
            QTextEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
            }
            QScrollArea {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
            }
            QCheckBox {
                color: white;
            }
            QMenuBar {
                background-color: #2d2d2d;
                color: white;
            }
            QMenuBar::item:selected {
                background-color: #0e639c;
            }
            QMenu {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
            }
            QMenu::item:selected {
                background-color: #0e639c;
            }
        """
        self.setStyleSheet(dark_stylesheet)
    
    def apply_light_theme(self):
        """Applique un thème clair"""
        self.setStyleSheet("")  # Réinitialiser au thème par défaut
    
    def show_about(self):
        """Affiche la boîte de dialogue À propos"""
        about_text = """
        <h2>Steam Price Checker V2</h2>
        <p><b>Version:</b> 2.0.0</p>
        <p><b>Développé avec:</b> PyQt6</p>
        <p>Récupérateur automatisé de prix Steam pour liste de jeux (DLC + Games + Prices)</p>
        <p><b>Fonctionnalités:</b></p>
        <ul>
            <li>Vérification des prix des jeux et DLC</li>
            <li>Sauvegarde/Chargement de listes</li>
            <li>Sélection de jeux avec checkboxes</li>
            <li>Liens cliquables vers le Steam Store</li>
            <li>Affichage des images de jeux</li>
            <li>Thème sombre et clair</li>
        </ul>
        <p><b>Discord:</b> <a href="https://discord.gg/Z9aKEWsGga">https://discord.gg/Z9aKEWsGga</a></p>
        <p><b>E-mail:</b> all.infiny@gmail.com</p>
        """
        QMessageBox.about(self, "À propos", about_text)
    
    def add_game_by_id(self):
        """Ajoute un jeu par son ID Steam"""
        appid = self.search_input.text().strip()
        if not appid.isdigit():
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un ID Steam valide (numérique)")
            return
        
        # Vérifier si le jeu n'est pas déjà dans la liste
        for game in self.games_data:
            if str(game.get('appid')) == appid:
                QMessageBox.information(self, "Information", "Ce jeu est déjà dans la liste")
                return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Mode indéterminé
        
        # Récupérer les informations du jeu
        game_info = get_steam_price_with_dlc(appid)
        
        self.progress_bar.setVisible(False)
        
        if game_info and 'error' not in game_info:
            self.games_data.append(game_info)
            self.add_game_widget(game_info)
            self.search_input.clear()
            QMessageBox.information(self, "Succès", f"Jeu '{game_info['title']}' ajouté!")
        else:
            error_msg = game_info.get('error', 'Erreur inconnue') if game_info else 'Impossible de récupérer les informations'
            QMessageBox.critical(self, "Erreur", f"Impossible d'ajouter le jeu: {error_msg}")
    
    def add_game_widget(self, game_info):
        """Ajoute un widget de jeu à l'interface"""
        game_widget = GameCheckBox(game_info)
        self.game_widgets.append(game_widget)
        self.games_layout.addWidget(game_widget)
    
    def load_file(self):
        """Charge un fichier .txt contenant des IDs Steam"""
        file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir fichier .txt", "", "Text Files (*.txt)")
        if file_name:
            try:
                with open(file_name, "r") as f:
                    appids = [line.strip() for line in f if line.strip().isdigit()]
                self.process_appids(appids)
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de lire le fichier : {str(e)}")
    
    def load_json(self):
        """Charge une liste sauvegardée au format JSON"""
        file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir fichier .json", "", "JSON Files (*.json)")
        if file_name:
            try:
                with open(file_name, "r", encoding='utf-8') as f:
                    data = json.load(f)
                    self.games_data = data.get('games', [])
                    
                    # Effacer les widgets existants
                    for widget in self.game_widgets:
                        widget.deleteLater()
                    self.game_widgets.clear()
                    
                    # Recréer les widgets
                    for game in self.games_data:
                        self.add_game_widget(game)
                    
                    QMessageBox.information(self, "Succès", f"{len(self.games_data)} jeu(x) chargé(s)")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de lire le fichier : {str(e)}")
    
    def save_json(self):
        """Sauvegarde la liste actuelle au format JSON"""
        if not self.games_data:
            QMessageBox.warning(self, "Attention", "Aucun jeu à sauvegarder")
            return
        
        file_name, _ = QFileDialog.getSaveFileName(self, "Sauvegarder fichier .json", "", "JSON Files (*.json)")
        if file_name:
            try:
                data = {
                    'version': '2.0',
                    'games': self.games_data
                }
                with open(file_name, "w", encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                QMessageBox.information(self, "Succès", "Liste sauvegardée avec succès!")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de sauvegarder le fichier : {str(e)}")
    
    def process_appids(self, appids):
        """Traite une liste d'IDs Steam"""
        # Effacer les données existantes
        for widget in self.game_widgets:
            widget.deleteLater()
        self.game_widgets.clear()
        self.games_data.clear()
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, len(appids))
        
        for i, appid in enumerate(appids):
            self.progress_bar.setValue(i)
            game_info = get_steam_price_with_dlc(appid)
            if game_info:
                self.games_data.append(game_info)
                self.add_game_widget(game_info)
            QApplication.processEvents()  # Garder l'interface réactive
        
        self.progress_bar.setVisible(False)
        self.result_area.setPlainText(f"✅ {len(self.games_data)} jeu(x) chargé(s)")
    
    def calculate_selected(self):
        """Calcule les prix des jeux sélectionnés"""
        total_with_discount = 0
        total_without_discount = 0
        result_text = ""
        selected_count = 0
        
        for i, game_widget in enumerate(self.game_widgets):
            if game_widget.is_checked():
                selected_count += 1
                game_info = self.games_data[i]
                
                if "error" in game_info:
                    result_text += f"❌ {game_info['title']} : Erreur - {game_info.get('error', 'Inconnue')}\n"
                    continue
                
                result_text += (
                    f"\n🎮 {game_info['title']}\n"
                    f"  🔗 {game_info.get('store_url', 'N/A')}\n"
                    f"  Prix original : {game_info['initial']:.2f} €\n"
                    f"  Prix actuel : {game_info['final']:.2f} € (-{game_info['discount_percent']}%)\n"
                )
                total_without_discount += game_info["initial"]
                total_with_discount += game_info["final"]
                
                # Traitement des DLC
                if game_info.get("dlcs"):
                    for dlc in game_info["dlcs"]:
                        result_text += (
                            f"    🧩 DLC - {dlc['title']}\n"
                            f"      🔗 {dlc.get('store_url', 'N/A')}\n"
                            f"      Prix original : {dlc['initial']:.2f} €\n"
                            f"      Prix actuel : {dlc['final']:.2f} € (-{dlc['discount_percent']}%)\n"
                        )
                        total_without_discount += dlc["initial"]
                        total_with_discount += dlc["final"]
        
        if selected_count == 0:
            QMessageBox.warning(self, "Attention", "Aucun jeu sélectionné")
            return
        
        result_text += "\n" + "=" * 70 + "\n"
        result_text += f"📊 Jeux sélectionnés : {selected_count}\n"
        result_text += f"💰 Total sans réduction : {total_without_discount:.2f} €\n"
        result_text += f"💸 Total avec réduction : {total_with_discount:.2f} €\n"
        result_text += f"🎉 Économies : {(total_without_discount - total_with_discount):.2f} € ({((total_without_discount - total_with_discount) / total_without_discount * 100 if total_without_discount > 0 else 0):.1f}%)\n"
        
        self.result_area.setPlainText(result_text)


def main():
    """Point d'entrée de l'application"""
    app = QApplication(sys.argv)
    app.setApplicationName("Steam Price Checker V2")
    app.setOrganizationName("SteamPy")
    
    window = SteamPriceApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
