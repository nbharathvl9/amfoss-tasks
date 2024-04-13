import sys
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QApplication, QMessageBox, QVBoxLayout, QDialog, QHBoxLayout
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import Qt
import requests

class PokemonViewer(QDialog):
    IMAGE_SIZE = (350, 350)  # Set a fixed size for all Pokémon images

    def __init__(self, parent=None, images=[], names=[]):
        super().__init__(parent)
        self.setWindowTitle("Pokémon")
        self.setWindowIcon(QIcon("assets/pokeball.png"))
        self.resize(380, 380)  # Adjust the dialog size to accommodate the fixed image size
        self.layout = QVBoxLayout(self)



        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(*self.IMAGE_SIZE)  # Set the size of the image label
        self.layout.addWidget(self.image_label)

        self.pokemon_name_label = QLabel(self)  # Create the QLabel widget
        self.layout.addWidget(self.pokemon_name_label)  # Add the label to the layout
        self.pokemon_name_label.setFont(QFont("Arial", 16))

        self.prev_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.prev_button.clicked.connect(self.show_previous)
        self.next_button.clicked.connect(self.show_next)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        self.layout.addLayout(button_layout)



        self.current_index = 0
        self.pokemon_images = images
        self.pokemon_names = names

    def set_pokemon_images(self, images, names):
        self.pokemon_images = images
        self.pokemon_names = names  # Set the pokemon_names attribute
        self.current_index = 0
        self.show_image()

    def show_image(self):
     if self.pokemon_images:
        pixmap = self.pokemon_images[self.current_index]
        scaled_pixmap = pixmap.scaled(*self.IMAGE_SIZE)  # Remove aspectRatioMode argument
        self.image_label.setPixmap(scaled_pixmap)
        if self.pokemon_names:
            self.pokemon_name_label.setText(self.pokemon_names[self.current_index])
        else:
            self.pokemon_name_label.setText("") 
     else:
        self.image_label.clear()
        self.pokemon_name_label.clear()

    def show_previous(self):
        if self.pokemon_images:
            self.current_index = (self.current_index - 1) % len(self.pokemon_images)
            self.show_image()

    def show_next(self):
        if self.pokemon_images:
            self.current_index = (self.current_index + 1) % len(self.pokemon_images)
            self.show_image()

class SearchWindow(QWidget):
    IMAGE_SIZE = (300, 300)  # Set a fixed size for all captured Pokémon images

    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 850, 500)
        self.setFixedSize(850, 500)
        self.setWindowTitle("PokeSearch")

        self.label = QLabel(self)
        pixmap = QPixmap("../assets/landing.jpg")
        self.label.setPixmap(pixmap)
        self.label.setGeometry(0, 0, self.width(), self.height())

        self.enter_name_label = QLabel("Any name of Pokemon", self)  # Label for entering name
        self.enter_name_label.setGeometry(50, 20, 280, 20)
        self.enter_name_label.setFont(QFont("Verdana", 12))

        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(50, 50, 280, 40)
        self.textbox.setPlaceholderText("Search Pokémon...")

        self.search_button = QPushButton("Search", self)
        self.search_button.setFont(QFont("Arial", 10))
        self.search_button.setGeometry(50, 300, 160, 43)
        self.search_button.clicked.connect(self.search_pokemon)

        self.capture_button = QPushButton("Capture", self)
        self.capture_button.setFont(QFont("Arial", 10))
        self.capture_button.setGeometry(50, 350, 160, 43)
        self.capture_button.clicked.connect(self.capture_pokemon)

        self.display_button = QPushButton("Display", self)
        self.display_button.setFont(QFont("Arial", 10))
        self.display_button.setGeometry(50, 400, 160, 43)
        self.display_button.clicked.connect(self.display_captured_pokemon)

        self.captured_pokemon = []
        self.captured_pokemon_images = []
        self.pokemon_names = []

        self.name_label = QLabel(self)
        self.name_label.setGeometry(400, 250, 300, 30)
        self.name_label.setFont(QFont("Arial", 12))

        self.abilities_label = QLabel(self)
        self.abilities_label.setGeometry(400, 270, 300, 30)
        self.abilities_label.setFont(QFont("Arial", 12))

        self.types_label = QLabel(self)
        self.types_label.setGeometry(400, 290, 300, 30)
        self.types_label.setFont(QFont("Arial", 12))

        self.stats_label = QLabel(self)
        self.stats_label.setGeometry(400, 310, 300, 200)
        self.stats_label.setFont(QFont("Arial", 12))

        self.pokemon_image_label = QLabel(self)
        self.pokemon_image_label.setGeometry(400, 0, 300, 270)

        self.last_clicked_button = None
        # Call the button style function
        self.set_button_style(self.search_button)
        self.set_button_style(self.capture_button)
        self.set_button_style(self.display_button)


    def set_button_style(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: gray;
                color: white;
                border-radius: 8px;
                border: 1px solid black;
            }
            QPushButton:hover {
                background-color: white;
                color: black;
                
            }
            QPushButton:pressed {
                background-color: red;
            }
        """)

    def button_clicked(self, button):
        if self.last_clicked_button:
            self.set_button_style(self.last_clicked_button)
        self.set_button_style(button)
        self.last_clicked_button = button

    def search_pokemon(self):
        pokemon_name = self.textbox.text().lower()
        pokemon_name = pokemon_name.replace(' ', '-')

        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            if 'sprites' in data and data['sprites'] and 'front_default' in data['sprites'] and data['sprites']['front_default']:
                image_url = data['sprites']['other']['official-artwork']['front_default']
                image_data = requests.get(image_url).content
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)

                self.pokemon_image_label.setPixmap(pixmap)
                self.pokemon_image_label.setScaledContents(True)
                name = data['species']['name']
                abilities = data['abilities']
                ability_names = [ability_info['ability']['name'] for ability_info in abilities]
                abilities_string = ', '.join(ability_names)

                types = data['types']
                type_names = [type_info['type']['name'] for type_info in types]

                stats_info = "Stats:\n"
                for stat_entry in data['stats']:
                    stat_name = stat_entry['stat']['name']
                    base_stat = stat_entry['base_stat']
                    stats_info += f"{stat_name}: {base_stat}\n"

                self.name_label.setText(f"Name: {name}")
                self.abilities_label.setText(f"Abilities: {abilities_string}")
                self.types_label.setText(f"Types: {', '.join(type_names)}")
                self.stats_label.setText(stats_info)

                self.label.hide()
            else:
                QMessageBox.warning(self, "Warning", "No image available for this Pokémon.")
        else:
            QMessageBox.warning(self, "Error", f"Could not find Pokémon '{pokemon_name}'")

    def capture_pokemon(self):
        self.button_clicked(self.capture_button)
        pokemon_name = self.textbox.text().lower()
        pokemon_name = pokemon_name.replace(' ', '-')

        if pokemon_name in self.captured_pokemon:
            QMessageBox.information(self, "Capture", f"Pokemon '{pokemon_name}' already captured!")
        else:
            url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

                if 'sprites' in data and data['sprites'] and 'front_default' in data['sprites'] and data['sprites']['front_default']:
                    image_url = data['sprites']['other']['official-artwork']['front_default']
                    image_data = requests.get(image_url).content
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)

                    self.captured_pokemon_images.append(pixmap)
                    self.captured_pokemon.append(pokemon_name)
                    self.pokemon_names.append(pokemon_name)

                    QMessageBox.information(self, "Capture", f"Captured Pokémon '{pokemon_name}' successfully.")

                else:
                    QMessageBox.warning(self, "Warning", "No image available for this Pokémon.")
            else:
                QMessageBox.warning(self, "Error", f"Could not find Pokémon '{pokemon_name}'")

    def display_captured_pokemon(self):
        if not self.captured_pokemon_images:
            QMessageBox.warning(self, "Warning", "No Pokémon images captured yet.")
            return

        pokemon_viewer = PokemonViewer(images=self.captured_pokemon_images, names=self.captured_pokemon)
        pokemon_viewer.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SearchWindow()
    window.show()
    sys.exit(app.exec_())
