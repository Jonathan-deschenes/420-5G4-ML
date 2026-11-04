import customtkinter as ctk

from views.composants import BLANC, BarreOnglets, BarreRecherche
from views.ecranLivre import EcranLivre
from views.ecranUtilisateur import EcranUtilisateur


PLACEHOLDER_LIVRES = "Rechercher par titre, auteur et isbn"
PLACEHOLDER_UTILISATEURS = "Rechercher par nom"


class App(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        super().__init__(fg_color=BLANC)

        self.title("Bibliothèque")
        self.geometry("920x900")
        self.minsize(820, 720)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.barre_recherche = BarreRecherche(self, PLACEHOLDER_LIVRES)
        self.barre_recherche.grid(row=0, column=0, sticky="ew")

        self.barre_onglets = BarreOnglets(self, self.afficher_ecran)
        self.barre_onglets.grid(row=1, column=0, sticky="ew")

        self.conteneur = ctk.CTkFrame(self, fg_color=BLANC, corner_radius=0)
        self.conteneur.grid(row=2, column=0, sticky="nsew")
        self.conteneur.grid_columnconfigure(0, weight=1)
        self.conteneur.grid_rowconfigure(0, weight=1)

        self.ecran_livre = EcranLivre(self.conteneur)
        self.ecran_utilisateur = EcranUtilisateur(
            self.conteneur,
            on_ajout=self._utilisateur_ajoute,
        )

        self.ecran_livre.grid(row=0, column=0, sticky="nsew")
        self.ecran_utilisateur.grid(row=0, column=0, sticky="nsew")
        self.ecran_utilisateur.grid_remove()

        self.afficher_ecran("livres")

    def afficher_ecran(self, nom):
        self.ecran_livre.fermer_menu_filtre()

        if nom == "livres":
            self.ecran_utilisateur.grid_remove()
            self.ecran_livre.grid()
            self.ecran_livre.tkraise()
            self.barre_recherche.definir_placeholder(PLACEHOLDER_LIVRES)
        else:
            self.ecran_livre.grid_remove()
            self.ecran_utilisateur.grid()
            self.ecran_utilisateur.tkraise()
            self.barre_recherche.definir_placeholder(PLACEHOLDER_UTILISATEURS)

        self.barre_recherche.effacer()
        self.barre_onglets.definir_actif(nom)

    def _utilisateur_ajoute(self):
        self.ecran_livre.ajouter_utilisateur()


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
