import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QWidget, QAction, QToolBar, QHBoxLayout, \
    QLabel, QGridLayout, QComboBox, QPushButton, QDialog, QInputDialog
from PyQt5.QtCore import Qt, QCoreApplication, QSize, QDir
from PyQt5.QtGui import QIcon, QPalette
import os


class Fenetre(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Générateur de PixelArt")
        self.setFixedSize(750, 900)

        self.affichage_gauche = QVBoxLayout()
        self.palette_grid = QGridLayout()
        self.grille = QGridLayout()
        self.affichage_droit = QVBoxLayout()
        self.tools = QHBoxLayout()
        self.page = QHBoxLayout()
        self.box_slider1 = QHBoxLayout()
        self.box_slider2 = QHBoxLayout()
        self.box_slider3 = QHBoxLayout()

        #Éléments de la partie gauche de l'affichage (QVBox)
        self.ma_couleur_label = QLabel("(Création de couleur)")
        self.ma_couleur_label.setAlignment(Qt.AlignCenter)

        self.slider_rouge = QSlider(Qt.Horizontal)
        self.slider_vert = QSlider(Qt.Horizontal)
        self.slider_bleu = QSlider(Qt.Horizontal)

        self.label_slider_rouge = QLabel("Rouge")
        self.label_slider_rouge.setStyleSheet("color: red")

        self.label_slider_vert = QLabel("Vert")
        self.label_slider_vert.setStyleSheet("color: green")

        self.label_slider_bleu = QLabel("Bleu")
        self.label_slider_bleu.setStyleSheet("color: blue")

        self.slider_rouge.setMinimum(0)
        self.slider_rouge.setMaximum(255)
        self.slider_vert.setMinimum(0)
        self.slider_vert.setMaximum(255)
        self.slider_bleu.setMinimum(0)
        self.slider_bleu.setMaximum(255)

        self.slider_rouge.valueChanged.connect(self.change_color)
        self.slider_bleu.valueChanged.connect(self.change_color)
        self.slider_vert.valueChanged.connect(self.change_color)

        self.outils_label = QLabel("Outils")
        self.outils_label.setStyleSheet("color: slategrey; font-size: 18px; font-weight: bold")
        self.outils_label.setAlignment(Qt.AlignCenter)
        self.couleurs_label = QLabel("Couleurs")
        self.couleurs_label.setStyleSheet("color: slategrey; font-size: 18px; font-weight: bold")
        self.couleurs_label.setAlignment(Qt.AlignCenter)

        self.box_slider1.addWidget(self.slider_rouge)
        self.box_slider1.addWidget(self.label_slider_rouge)
        self.box_slider_label_widget1 = QWidget()
        self.box_slider_label_widget1.setLayout(self.box_slider1)

        self.box_slider2.addWidget(self.slider_vert)
        self.box_slider2.addWidget(self.label_slider_vert)
        self.box_slider_label_widget2 = QWidget()
        self.box_slider_label_widget2.setLayout(self.box_slider2)

        self.box_slider3.addWidget(self.slider_bleu)
        self.box_slider3.addWidget(self.label_slider_bleu)
        self.box_slider_label_widget3 = QWidget()
        self.box_slider_label_widget3.setLayout(self.box_slider3)

        btn_ajout = QPushButton("Ajouter à la palette")
        btn_ajout.clicked.connect(self.afficher_popup)
        btn_ajout.setFixedSize(225, 50)
        btn_ajout.setStyleSheet("font-size: 14px; font-weight: bold")

        self.affichage_gauche.addWidget(self.outils_label)
        self.affichage_gauche.addWidget(self.couleurs_label)
        self.affichage_gauche.addLayout(self.palette_grid)
        self.affichage_gauche.addWidget(self.box_slider_label_widget1)
        self.affichage_gauche.addWidget(self.box_slider_label_widget2)
        self.affichage_gauche.addWidget(self.box_slider_label_widget3)
        self.affichage_gauche.addWidget(self.ma_couleur_label)
        self.affichage_gauche.addWidget(btn_ajout)

        self.palette_grid.setSpacing(2)
        self.list_couleurs_default = [(0, 0, 0), (147, 32, 255), (0, 0, 255), (255, 153, 0), (255, 0, 0), (255, 255, 0),
                                      (0, 104, 0), (171, 220, 244), (255, 255, 255), (255, 208, 198)]
        self.list_filtre_rouge = [(255, 0, 0), (255, 94, 95), (255, 51, 94), (128, 0, 0), (220, 20, 60), (255, 97, 131),
                                  (255, 23, 131), (205, 92, 92), (240, 128, 128), (255, 124, 95)]
        self.list_filtre_vert = [(107, 142, 35), (85, 107, 47), (128, 128, 0), (46, 139, 87), (32, 178, 170),
                                 (60, 179, 113), (152, 251, 152), (0, 255, 0), (173, 255, 47), (34, 139, 34)]
        self.list_filtre_bleu = [(72, 61, 139), (230, 230, 250), (176, 224, 230), (135, 206, 250), (0, 191, 255),
                                 (30, 144, 255), (100, 149, 237), (123, 104, 238), (65, 105, 225), (0, 0, 205)]
        self.list_filtre_negatif = [(15, 164, 250), (0, 255, 247), (0, 255, 154), (220, 232, 255), (162, 255, 0),
                                    (0, 204, 204), (171, 255, 135), (192, 192, 192), (32, 32, 32), (0, 153, 153)]
        self.list_filtre_gris = [(121, 128, 129), (90, 94, 107), (220, 220, 220), (119, 136, 153), (112, 128, 144),
                                 (192, 192, 192), (209, 197, 197), (146, 122, 122), (131, 113, 113), (94, 77, 77)]

        indice = 0
        for i in range(5):
            for j in range(2):
                self.couleur = QPushButton()
                self.couleur.setFixedSize(50, 50)
                self.couleur.setStyleSheet(
                    f"background-color:rgb{self.list_couleurs_default[indice]};border: 1px solid black")
                self.couleur.clicked.connect(lambda event, row=i, col=j: self.recup_couleur_palette(row, col))
                self.palette_grid.addWidget(self.couleur, i, j)

                indice += 1

        #Éléments de la partie droite de l'affichage (QVBox)
        self.grille.setSpacing(1)

        self.lignes = 12
        self.colonnes = 12

        for i in range(self.lignes):
            for j in range(self.colonnes):
                self.coord = QLabel()
                self.coord.setStyleSheet("background-color:white; border: 1px solid black")
                self.coord.mousePressEvent = lambda event, row=i, col=j: self.colorier(row, col)
                self.grille.addWidget(self.coord, i, j)

        self.outils = QComboBox()
        self.outils.addItem("Stylo")
        self.outils.addItem("Gomme")
        self.outils.addItem("Baguette")
        self.outils.addItem("Pot")
        self.outils.setFixedSize(200, 50)
        self.outils.setStyleSheet("font-size: 14px; font-weight: bold")
        self.outils.activated[str].connect(self.choix_tools)

        self.couleur_actuelle = QLabel()
        self.couleur_actuelle.setStyleSheet("background-color: white ; border: 1px solid black")
        self.couleur_actuelle.setFixedSize(50, 50)

        self.predef = QComboBox()
        #self.predef.addItem("Fleur")
        #self.predef.addItem("Arbre")
        self.predef.setFixedSize(200, 50)
        self.predef.setStyleSheet("font-size: 14px; font-weight: bold")
        self.remplirPredef()
        self.predef.activated[str].connect(self.choix_predefs)

        self.tools.addWidget(self.outils)
        self.tools.addWidget(self.couleur_actuelle)
        self.tools.addWidget(self.predef)

        self.affichage_droit.addLayout(self.tools)
        self.affichage_droit.addLayout(self.grille)

        #Configuration de la Menu Bar
        self.menu = self.menuBar()

        self.reinitialiser_action = QAction(QIcon("reset.png"), "Réinitialiser", self)
        self.reinitialiser_action.triggered.connect(self.onReset)
        self.reinitialiser_action.setShortcut('Ctrl+D')

        self.reinitialiser_palette_action = QAction(QIcon("reset_palette.png"), "Réinitialiser la palette", self)
        self.reinitialiser_palette_action.triggered.connect(self.onResetPalette)
        self.reinitialiser_palette_action.setShortcut('Ctrl+P')

        self.menuGrille = self.menu.addMenu("&Grille")
        self.menuGrille.addAction(self.reinitialiser_action)
        self.menuGrille.addAction(self.reinitialiser_palette_action)

        self.filtre_rouge = QAction(QIcon("cercle_rouge.png"), "Filtre rouge", self)
        self.filtre_rouge.triggered.connect(self.filtration_rouge)
        self.filtre_rouge.setShortcut('Ctrl+R')

        self.filtre_vert = QAction(QIcon("cercle_vert.png"), "Filtre vert", self)
        self.filtre_vert.triggered.connect(self.filtration_verte)
        self.filtre_vert.setShortcut('Ctrl+V')

        self.filtre_bleu = QAction(QIcon("cercle_bleu.png"), "Filtre bleu", self)
        self.filtre_bleu.triggered.connect(self.filtration_bleu)
        self.filtre_bleu.setShortcut('Ctrl+B')

        self.filtre_negatif = QAction(QIcon("cercle_negatif.png"), "Filtre négatif", self)
        self.filtre_negatif.triggered.connect(self.filtration_negatif)
        self.filtre_negatif.setShortcut('Ctrl+N')

        self.filtre_gris = QAction(QIcon("cercle_gris.png"), "Filtre gris", self)
        self.filtre_gris.triggered.connect(self.filtration_gris)
        self.filtre_gris.setShortcut('Ctrl+G')

        self.menuFiltre = self.menu.addMenu("&Filtre")
        self.menuFiltre.addAction(self.filtre_rouge)
        self.menuFiltre.addAction(self.filtre_vert)
        self.menuFiltre.addAction(self.filtre_bleu)
        self.menuFiltre.addSeparator()
        self.menuFiltre.addAction(self.filtre_negatif)
        self.menuFiltre.addAction(self.filtre_gris)

        self.effet_noir_et_blanc = QAction(QIcon("black-and-white.png"), "Effet Noir et Blanc", self)
        self.effet_noir_et_blanc.triggered.connect(self.effet_n_et_b)
        self.effet_noir_et_blanc.setShortcut('Ctrl+E')

        self.menuEffet = self.menu.addMenu("&Effets")
        self.menuEffet.addAction(self.effet_noir_et_blanc)

        self.sauvegarder_action = QAction(QIcon("sauvegarde.png"), "Sauvegarder", self)
        self.sauvegarder_action.triggered.connect(self.onSave)
        self.sauvegarder_action.setShortcut('Ctrl+S')

        self.menuSauvegarder = self.menu.addMenu("&Sauvegarder")
        self.menuSauvegarder.addAction(self.sauvegarder_action)

        self.quitter_action = QAction(QIcon("quitter.png"), "Quitter", self)
        self.quitter_action.triggered.connect(self.onExit)
        self.quitter_action.setShortcut('Ctrl+Q')

        self.menuQuitter = self.menu.addMenu("&Quitter")
        self.menuQuitter.addAction(self.quitter_action)

        #Configuration de la Tool Bar
        self.toolbar = QToolBar("Ma toolbar")
        self.toolbar.setIconSize(QSize(48, 48))
        self.addToolBar(self.toolbar)

        self.reinitialiser_action.setToolTip("Réinitialiser")  # Infobulle
        self.reinitialiser_palette_action.setToolTip("Réinitialiser la palette")
        self.filtre_rouge.setToolTip("Filtre rouge")
        self.filtre_vert.setToolTip("Filtre vert")
        self.filtre_bleu.setToolTip("Filtre bleu")
        self.filtre_negatif.setToolTip("Filtre négatif")
        self.filtre_gris.setToolTip("Filtre gris")
        self.effet_noir_et_blanc.setToolTip("Effet Noir et Blanc")
        self.sauvegarder_action.setToolTip("Sauvegarder")
        self.quitter_action.setToolTip("Quitter")

        self.toolbar.addAction(self.reinitialiser_action)
        self.toolbar.addAction(self.reinitialiser_palette_action)
        self.toolbar.addAction(self.filtre_rouge)
        self.toolbar.addAction(self.filtre_vert)
        self.toolbar.addAction(self.filtre_bleu)
        self.toolbar.addAction(self.filtre_negatif)
        self.toolbar.addAction(self.filtre_gris)
        self.toolbar.addAction(self.effet_noir_et_blanc)
        self.toolbar.addAction(self.sauvegarder_action)
        self.toolbar.addAction(self.quitter_action)

        #Rassemble dans le Layout page l'affichage gauche et droit (QHBox)
        self.page.addLayout(self.affichage_gauche)
        self.page.addLayout(self.affichage_droit)

        self.widget = QWidget()
        self.widget.setLayout(self.page)
        self.setCentralWidget(self.widget)

    def change_color(self):
        self.val_rouge = self.slider_rouge.value()
        self.val_vert = self.slider_vert.value()
        self.val_bleu = self.slider_bleu.value()

        self.label_slider_rouge.setText(str(self.val_rouge))
        self.label_slider_vert.setText(str(self.val_vert))
        self.label_slider_bleu.setText(str(self.val_bleu))

        # Utilise fonctionnalité des f-strings, car .setText() ne peut prendre qu'un seul paramètre
        self.ma_couleur_label.setText(f"rgb({str(self.val_rouge)};{str(self.val_vert)};{str(self.val_bleu)})")
        self.ma_couleur_label.setStyleSheet(
            f"background-color: rgb({str(self.val_rouge)},{self.val_vert},{self.val_bleu}) ; border: 2px solid black")

    def recup_couleur_palette(self, row, col):

        bouton = self.palette_grid.itemAtPosition(row,
                                                  col).widget()  #Récupère le btn qui se trouvant en position row col dans la grille palette
        couleur = bouton.palette().color(QPalette.Background)  #Récupère la couleur de ce bouton

        self.couleur_rouge = couleur.red()  #Récupère la val rouge, bleu et verte de la couleur du bouton
        self.couleur_verte = couleur.green()
        self.couleur_bleu = couleur.blue()
        self.couleur_actuelle.setStyleSheet(
            f"background-color: rgb({self.couleur_rouge},{self.couleur_verte},{self.couleur_bleu}); border: 2px solid black")

    def colorier(self, row, col):
        if self.outils.currentText() == "Stylo":
            coord = self.grille.itemAtPosition(row, col).widget()

            coord.setStyleSheet(
                f"background-color: rgb({self.couleur_rouge},{self.couleur_verte},{self.couleur_bleu}) ; border: 1px solid black")

        elif self.outils.currentText() == "Gomme":
            coord = self.grille.itemAtPosition(row, col).widget()
            coord.setStyleSheet(f"background-color:white; border: 1px solid black")

    def choix_tools(self, text):
        if text == "Baguette":
            for i in range(self.lignes):
                for j in range(self.colonnes):

                    case = self.grille.itemAtPosition(i, j).widget()
                    col = case.palette().color(QPalette.Background)
                    col_rouge = col.red()
                    col_verte = col.green()
                    col_bleu = col.blue()
                    if self.couleur_rouge == col_rouge and self.couleur_verte == col_verte and self.couleur_bleu == col_bleu:
                        case.setStyleSheet("background-color:white; border: 1px solid black")


        elif text == "Pot":
            for i in range(self.lignes):
                for j in range(self.colonnes):
                    case = self.grille.itemAtPosition(i, j).widget()
                    col = case.palette().color(QPalette.Background)
                    col_rouge = col.red()
                    col_verte = col.green()
                    col_bleu = col.blue()

                    if col_rouge == 255 and col_verte == 255 and col_bleu == 255:
                        case.setStyleSheet(
                            f"background-color: rgb({self.couleur_rouge},{self.couleur_verte},{self.couleur_bleu}); border: 1px solid black")

    def choix_predefs(self, text):

        #print(text)
        pixelArtTxt = open(text, "r")
        pixelArt = pixelArtTxt.readlines()
        pixelArtTxt.close()

        for pixel in pixelArt:
            info = pixel.split()
            print(info)
            btn = self.grille.itemAtPosition(info[0], info[1]).widget()
            btn.setStyleSheet(f"background-color: rgb({info[2]},{info[3]},{info[4]}); border: 1px solid black")

    def afficher_popup(self):

        self.popup = QDialog()  #Fenêtre popup pour changer la palette
        pal_box = QHBoxLayout()
        sous_page_box = QVBoxLayout()

        for i in range(5):
            for j in range(2):
                coord = self.palette_grid.itemAtPosition(i, j).widget()
                couleur = coord.palette().color(QPalette.Background)

                button = QPushButton()
                button.setFixedSize(25, 25)
                button.setStyleSheet(f"background-color: {couleur.name()} ; border: 1px solid black")
                button.clicked.connect(lambda event, row=i, col=j: self.couleur_a_remplacer(row, col))
                pal_box.addWidget(button)

        sous_page_box.addWidget(QLabel("Choisissez la couleur à remplacer: "))
        sous_page_box.addLayout(pal_box)
        self.popup.setLayout(sous_page_box)

        self.popup.exec()

    def onReset(self):
        for i in range(self.lignes):
            for j in range(self.colonnes):
                case = self.grille.itemAtPosition(i, j).widget()
                case.setStyleSheet("background-color:white; border: 1px solid black")

    def onResetPalette(self):
        indice = 0
        for i in range(5):
            for j in range(2):
                coord = self.palette_grid.itemAtPosition(i, j).widget()
                coord.setStyleSheet(
                    f"background-color:rgb{self.list_couleurs_default[indice]}; border: 1px solid black")

                indice += 1

    def filtration_rouge(self):
        indice = 0
        for i in range(5):
            for j in range(2):
                coord = self.palette_grid.itemAtPosition(i, j).widget()
                coord.setStyleSheet(
                    f"background-color:rgb{self.list_filtre_rouge[indice]}; border: 1px solid black")

                indice += 1

    def filtration_verte(self):
        indice = 0
        for i in range(5):
            for j in range(2):
                coord = self.palette_grid.itemAtPosition(i, j).widget()
                coord.setStyleSheet(
                    f"background-color:rgb{self.list_filtre_vert[indice]}; border: 1px solid black")

                indice += 1

    def filtration_bleu(self):
        indice = 0
        for i in range(5):
            for j in range(2):
                coord = self.palette_grid.itemAtPosition(i, j).widget()
                coord.setStyleSheet(f"background-color:rgb{self.list_filtre_bleu[indice]}; border: 1px solid black")

                indice += 1

    def filtration_negatif(self):
        indice = 0
        for i in range(5):
            for j in range(2):
                coord = self.palette_grid.itemAtPosition(i, j).widget()
                coord.setStyleSheet(f"background-color:rgb{self.list_filtre_negatif[indice]}; border: 1px solid black")

                indice += 1

    def filtration_gris(self):
        indice = 0
        for i in range(5):
            for j in range(2):
                coord = self.palette_grid.itemAtPosition(i, j).widget()
                coord.setStyleSheet(f"background-color:rgb{self.list_filtre_gris[indice]}; border: 1px solid black")

                indice += 1

    def couleur_a_remplacer(self, row, col):
        coord = self.palette_grid.itemAtPosition(row, col).widget()
        coord.setStyleSheet(
            f"background-color: rgb({self.val_rouge},{self.val_vert},{self.val_bleu}); border: 1px solid black")
        self.popup.accept()

    def onSave(self):
        text, ok = QInputDialog.getText(self, "Enregistrement de création", "Entrez le nom de votre création: ")
        if ok:
            self.predef.addItem(text)
            file = open(text + ".txt", "w")  #Crée un fichier texte avec nommé le nom de la création
            for i in range(self.lignes):
                for j in range(self.colonnes):
                    case = self.grille.itemAtPosition(i, j).widget()
                    couleur = case.palette().color(QPalette.Background)
                    col_rouge = couleur.red()
                    col_verte = couleur.green()
                    col_bleu = couleur.blue()
                    file.write(str(i) + " " + str(j) + " " + str(col_rouge) + " " + str(col_verte) + " " + str(
                        col_bleu) + "\n")
                    #Pour chaque case, on va lui créer un fichier texte avec les coordonnées et les valeurs rouge, verte et bleu de sa couleur

            file.close()

    def remplirPredef(
            self):  #Fonction executée dès le départ pour remplire la QComboBox avec les créations déjà existantes
        repertoire = QDir.currentPath()  #Donne chemin du répertoire de travail actuel
        #print(repertoire)
        for file in os.listdir(repertoire):  #Donne liste de fichiers dans le dossier en question
            if file.endswith(
                    ".txt"):  #Créations PixelArts sont stockées dans des fichiers texte, vérifie si c'est un fichier format texte
                self.predef.addItem(file[:-4])  #Rajoute à QComboBox (affichage)

    def effet_n_et_b(self):
        for i in range(self.lignes):
            for j in range(self.colonnes):
                case = self.grille.itemAtPosition(i, j).widget()
                col = case.palette().color(QPalette.Background)
                col_rouge = col.red()
                col_verte = col.green()
                col_bleu = col.blue()

                moy = (col_rouge + col_verte + col_bleu) // 3

                if moy > 170 and moy != 255:
                    case.setStyleSheet("background-color:lightgray; border: 1px solid black")

                elif 170 >= moy > 85:
                    case.setStyleSheet("background-color:grey; border: 1px solid black")


                elif moy <= 85:
                    case.setStyleSheet("background-color:black; border: 1px solid black")

    def onExit(self):
        sys.exit()


app = QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)

window = Fenetre()
window.show()

app.exec_()
