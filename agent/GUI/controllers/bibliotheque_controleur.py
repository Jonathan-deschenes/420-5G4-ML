import os
from datetime import datetime
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
        on_etat_change=None,
    ):
        if chemin_donnees is None:
            chemin_donnees = (
                os.environ.get("BIBLIOTHEQUE_DATA_DIR")
                or CHEMIN_DONNEES_DEFAUT
            )

        self.chemin_donnees = Path(chemin_donnees)
        self.chemin_livres = self.chemin_donnees / "books.txt"
        self.chemin_utilisateurs = self.chemin_donnees / "users.txt"

        self.persistance = persistance
        self.auto_sauvegarde = persistance and auto_sauvegarde
        self.on_etat_change = on_etat_change
        self.derniere_sauvegarde = None
        self.derniere_erreur = None
        self.dernier_message = None
        self.vues = []

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
            self.derniere_erreur = self.filemanager.last_error or None

    def definir_callback_etat(self, callback):
        self.on_etat_change = callback
        self._notifier_etat()

    def attacher_vues(self, *vues):
        self.vues = [vue for vue in vues if vue is not None]

    def _notifier_etat(self):
        if self.on_etat_change is not None:
            self.on_etat_change(self.etat_persistance())

    def _rafraichir_vues(self):
        for vue in self.vues:
            try:
                if vue.winfo_exists():
                    vue.rafraichir()
            except Exception:
                continue

    def _sur_modification(self):
        if self.auto_sauvegarde:
            self.sauvegarder()
        self._rafraichir_vues()

    def etat_persistance(self):
        return {
            "actif": self.persistance,
            "dossier": str(self.chemin_donnees),
            "fichiers": {
                "livres": str(self.chemin_livres),
                "utilisateurs": str(self.chemin_utilisateurs),
            },
            "existent": {
                "livres": self.chemin_livres.exists(),
                "utilisateurs": self.chemin_utilisateurs.exists(),
            },
            "derniere_sauvegarde": self.derniere_sauvegarde,
            "derniere_erreur": self.derniere_erreur,
            "dernier_message": self.dernier_message,
            "contenu": {
                "livres": self.bibliotheque.get_total_books(),
                "utilisateurs": len(self.bibliotheque.get_all_users()),
            },
        }

    def sauvegarder(self):
        if self.filemanager is None:
            return False

        try:
            self.chemin_donnees.mkdir(parents=True, exist_ok=True)
        except OSError as erreur:
            self.derniere_erreur = (
                f"Impossible de créer le dossier {self.chemin_donnees} : {erreur}"
            )
            self._notifier_etat()
            return False

        try:
            succes = self.filemanager.save_library_data(self.bibliotheque)
            erreur = self.filemanager.last_error
        except Exception as exception:
            succes = False
            erreur = str(exception)

        if succes:
            self.derniere_sauvegarde = datetime.now()
            self.derniere_erreur = None
            self.dernier_message = None
        else:
            self.derniere_erreur = erreur or "La sauvegarde a échoué."
            self.dernier_message = None

        self._notifier_etat()
        return succes

    def creer_backup(self):
        if self.filemanager is None:
            return False

        try:
            succes = self.filemanager.create_backup()
            erreur = self.filemanager.last_error
        except Exception as exception:
            succes = False
            erreur = str(exception)

        if succes:
            self.derniere_erreur = None
            self.dernier_message = "Sauvegarde de secours créée."
        else:
            self.derniere_erreur = erreur or "La sauvegarde de secours a échoué."
            self.dernier_message = None

        self._notifier_etat()
        return succes

    def fermer(self):
        if not self.persistance:
            return True
        return self.sauvegarder()

    def statistiques(self):
        return {
            "total": self.bibliotheque.get_total_books(),
            "disponibles": self.bibliotheque.get_available_book_count(),
            "empruntes": self.bibliotheque.get_checked_out_book_count(),
            "utilisateurs": len(self.bibliotheque.get_all_users()),
        }
