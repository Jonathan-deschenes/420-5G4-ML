import customtkinter as ctk

from views.composants import (
    BLANC,
    GRIS,
    GRIS_CLAIR,
    NOIR,
    TEXTE,
    VERT,
    BoutonRond,
    ModaleAjout,
    afficher_erreur,
    police,
)


class EcranUtilisateur(ctk.CTkFrame):
    def __init__(self, master, bibliotheque):
        super().__init__(master, fg_color=BLANC, corner_radius=0)
        self.bibliotheque = bibliotheque
        self.utilisateurs = []
        self.recherche = ""

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._construire()
        self._charger_donnees()
        self._afficher_lignes()

    def _construire(self):
        actions = ctk.CTkFrame(self, fg_color=BLANC, corner_radius=0)
        actions.grid(row=0, column=0, sticky="ew", padx=44, pady=(28, 18))

        ctk.CTkButton(
            actions,
            text="+  Ajouter un utilisateur",
            command=self.ouvrir_ajout,
            width=240,
            height=42,
            corner_radius=21,
            fg_color=NOIR,
            hover_color="#2C2C2C",
            text_color=BLANC,
            font=police(14),
        ).pack(side="left")

        self.liste = ctk.CTkScrollableFrame(
            self,
            fg_color=BLANC,
            corner_radius=0,
            scrollbar_fg_color=BLANC,
            scrollbar_button_color="#E4E4E4",
            scrollbar_button_hover_color="#CFCFCF",
        )
        self.liste.grid(row=1, column=0, sticky="nsew")
        self.liste.grid_columnconfigure(0, weight=1)

    def _charger_donnees(self):
        self.utilisateurs = self.bibliotheque.utilisateurs.lister(
            recherche=self.recherche
        )

    def rafraichir(self):
        self._charger_donnees()
        self._afficher_lignes()

    def rechercher(self, texte):
        self.recherche = texte
        self.rafraichir()

    def _afficher_lignes(self):
        for enfant in self.liste.winfo_children():
            enfant.destroy()

        if not self.utilisateurs:
            ctk.CTkLabel(
                self.liste,
                text="Aucun utilisateur à afficher",
                font=police(14),
                text_color=GRIS,
            ).grid(row=0, column=0, pady=40)
            return

        for index, utilisateur in enumerate(self.utilisateurs):
            fond = GRIS_CLAIR if index % 2 == 0 else BLANC
            ligne = ctk.CTkFrame(
                self.liste,
                fg_color=fond,
                corner_radius=0,
                height=68,
            )
            ligne.grid(row=index, column=0, sticky="ew")
            ligne.grid_columnconfigure(0, weight=1)
            ligne.grid_rowconfigure(0, weight=1)
            ligne.grid_propagate(False)

            ctk.CTkLabel(
                ligne,
                text=utilisateur["nom"],
                font=police(16),
                text_color=TEXTE,
                anchor="w",
                height=24,
            ).grid(row=0, column=0, sticky="w", padx=(44, 0))

            livres = utilisateur["livres"]
            if not livres:
                continue

            actions = ctk.CTkFrame(ligne, fg_color=fond, corner_radius=0)
            actions.grid(row=0, column=1, sticky="e", padx=(0, 44))

            for livre in livres:
                bloc = ctk.CTkFrame(actions, fg_color=fond, corner_radius=0)
                bloc.pack(side="right", padx=(14, 0))

                BoutonRond(
                    bloc,
                    "retour",
                    lambda utilisateur_cible=utilisateur, livre_cible=livre: (
                        self._rendre_livre(utilisateur_cible, livre_cible)
                    ),
                    fond=fond,
                    couleur_fond=NOIR,
                    couleur_survol="#2C2C2C",
                    taille=30,
                    taille_icone=16,
                ).pack(side="right")

                ctk.CTkLabel(
                    bloc,
                    text=livre["titre"],
                    width=200,
                    height=32,
                    corner_radius=16,
                    fg_color=VERT,
                    text_color=BLANC,
                    font=police(13),
                ).pack(side="right", padx=(0, 8))

    def _rendre_livre(self, utilisateur, livre):
        if not self.bibliotheque.utilisateurs.retourner_livre(
            utilisateur["identifiant"],
            livre["isbn"],
        ):
            afficher_erreur(
                f"Impossible de retourner « {livre['titre']} »."
            )

    def ouvrir_ajout(self):
        champs = [
            ("nom", "Nom", "Ex. : Marie Dubois"),
            ("identifiant", "ID utilisateur", "Ex. : USR026"),
        ]
        ModaleAjout(
            self.winfo_toplevel(),
            "Ajouter un utilisateur",
            champs,
            self._ajouter_utilisateur,
        )

    def _ajouter_utilisateur(self, donnees):
        try:
            self.bibliotheque.utilisateurs.ajouter(
                donnees["nom"],
                donnees["identifiant"],
            )
        except ValueError as erreur:
            afficher_erreur(str(erreur))
            return False
        return True
