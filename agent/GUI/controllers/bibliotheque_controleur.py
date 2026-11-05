from pathlib import Path

from models import FileManager, Library

from .livre_controleur import LivreControleur
from .utilisateur_controleur import UtilisateurControleur


CHEMIN_DONNEES_DEFAUT = Path(__file__).resolve().parents[2] / "data"


class BibliothequeControleur:
    def __init__(
        self,
        chemin_donnees=None,
        charger=True,
        persistance=True,
        auto_sauvegarde=True,
    ):
        if chemin_donnees is None:
            chemin_donnees = CHEMIN_DONNEES_DEFAUT

        self.chemin_donnees = Path(chemin_donnees)
        self.chemin_livres = self.chemin_donnees / "books.txt"
        self.chemin_utilisateurs = self.chemin_donnees / "users.txt"

        self.persistance = persistance
        self.auto_sauvegarde = persistance and auto_sauvegarde

        if persistance:
            self.filemanager = FileManager(
                str(self.chemin_livres),
                str(self.chemin_utilisateurs),
            )
        else:
            self.filemanager = None

        self.bibliotheque = Library()
        self.livres = LivreControleur(
            self.bibliotheque,
            self._sur_modification,
        )
        self.utilisateurs = UtilisateurControleur(
            self.bibliotheque,
            self._sur_modification,
        )

        if charger and self.filemanager is not None:
            self.filemanager.load_library_data(self.bibliotheque)

    def _sur_modification(self):
        if self.auto_sauvegarde:
            self.sauvegarder()

    def sauvegarder(self):
        if self.filemanager is None:
            return False
        return self.filemanager.save_library_data(self.bibliotheque)

    def creer_backup(self):
        if self.filemanager is None:
            return False
        try:
            self.filemanager.create_backup()
        except Exception:
            return False
        return True

    def statistiques(self):
        return {
            "total": self.bibliotheque.get_total_books(),
            "disponibles": self.bibliotheque.get_available_book_count(),
            "empruntes": self.bibliotheque.get_checked_out_book_count(),
            "utilisateurs": len(self.bibliotheque.get_all_users()),
        }
