from tkinter import messagebox

import customtkinter as ctk

from controllers import BibliothequeControleur
from views.composants import (
    BLANC,
    BarreEtat,
    BarreOnglets,
    BarreRecherche,
    afficher_erreur,
)
from views.ecranLivre import EcranLivre
from views.ecranUtilisateur import EcranUtilisateur


PLACEHOLDER_LIVRES = "Rechercher par titre, auteur et isbn"
PLACEHOLDER_UTILISATEURS = "Rechercher par nom ou identifiant"


class App(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        super().__init__(fg_color=BLANC)

        self.title("Bibliothèque")
        self.geometry("920x900")
        self.minsize(820, 720)

        self.bibliotheque = BibliothequeControleur()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.barre_recherche = BarreRecherche(
            self,
            PLACEHOLDER_LIVRES,
            on_change=self._rechercher,
        )
        self.barre_recherche.grid(row=0, column=0, sticky="ew")

        self.barre_onglets = BarreOnglets(self, self.afficher_ecran)
        self.barre_onglets.grid(row=1, column=0, sticky="ew")

        self.conteneur = ctk.CTkFrame(self, fg_color=BLANC, corner_radius=0)
        self.conteneur.grid(row=2, column=0, sticky="nsew")
        self.conteneur.grid_columnconfigure(0, weight=1)
        self.conteneur.grid_rowconfigure(0, weight=1)

        self.barre_etat = BarreEtat(
            self,
            self._sauvegarder,
            self._creer_backup,
        )
        self.barre_etat.grid(row=3, column=0, sticky="ew")

        self.ecran_livre = EcranLivre(self.conteneur, self.bibliotheque)
        self.ecran_utilisateur = EcranUtilisateur(
            self.conteneur,
            self.bibliotheque,
        )

        self.ecran_livre.grid(row=0, column=0, sticky="nsew")
        self.ecran_utilisateur.grid(row=0, column=0, sticky="nsew")
        self.ecran_utilisateur.grid_remove()

        self.bibliotheque.attacher_vues(
            self.ecran_livre,
            self.ecran_utilisateur,
        )
        self.bibliotheque.definir_callback_etat(self._maj_barre_etat)

        self.ecran_actif = self.ecran_livre
        self.afficher_ecran("livres")

        self.protocol("WM_DELETE_WINDOW", self._fermer)
        self.bind_all("<Control-s>", self._raccourci_sauvegarder)

        if self.bibliotheque.derniere_erreur:
            self.after(
                200,
                lambda: afficher_erreur(self.bibliotheque.derniere_erreur),
            )

    def _maj_barre_etat(self, etat=None):
        if etat is None:
            etat = self.bibliotheque.etat_persistance()

        if not etat["actif"]:
            self.barre_etat.afficher_etat("Persistance désactivée")
            return

        contenu = etat["contenu"]
        texte = (
            f"Données : {etat['dossier']} · "
            f"{contenu['livres']} livre(s) · "
            f"{contenu['utilisateurs']} utilisateur(s)"
        )

        sauvegarde = etat["derniere_sauvegarde"]
        if sauvegarde is not None:
            texte += f" · Enregistré à {sauvegarde.strftime('%H:%M:%S')}"

        message = etat["dernier_message"]
        if message:
            texte += f" · {message}"

        erreur = etat["derniere_erreur"]
        if erreur:
            texte += f" · {erreur}"

        self.barre_etat.afficher_etat(texte, erreur=bool(erreur))

    def _sauvegarder(self):
        if not self.bibliotheque.persistance:
            return False
        if not self.bibliotheque.sauvegarder():
            afficher_erreur(
                self.bibliotheque.derniere_erreur
                or "La sauvegarde a échoué."
            )
            return False
        return True

    def _creer_backup(self):
        if not self.bibliotheque.persistance:
            return False
        if not self.bibliotheque.creer_backup():
            afficher_erreur(
                self.bibliotheque.derniere_erreur
                or "La sauvegarde de secours a échoué."
            )
            return False
        return True

    def _raccourci_sauvegarder(self, _event=None):
        self._sauvegarder()
        return "break"

    def _fermer(self):
        if self.bibliotheque.persistance and not self.bibliotheque.fermer():
            if not messagebox.askyesno(
                "Sauvegarde",
                "La sauvegarde a échoué. Voulez-vous quitter sans enregistrer ?",
                parent=self,
            ):
                return
        self.destroy()

    def afficher_ecran(self, nom):
        self.ecran_livre.fermer_menu_filtre()

        if nom == "livres":
            self.ecran_actif = self.ecran_livre
            self.ecran_utilisateur.grid_remove()
            self.ecran_livre.grid()
            self.ecran_livre.tkraise()
            self.barre_recherche.definir_placeholder(PLACEHOLDER_LIVRES)
        else:
            self.ecran_actif = self.ecran_utilisateur
            self.ecran_livre.grid_remove()
            self.ecran_utilisateur.grid()
            self.ecran_utilisateur.tkraise()
            self.barre_recherche.definir_placeholder(PLACEHOLDER_UTILISATEURS)

        self.barre_recherche.effacer()
        self.ecran_actif.rechercher("")
        self.barre_onglets.definir_actif(nom)

    def _rechercher(self, texte):
        self.ecran_actif.rechercher(texte)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
