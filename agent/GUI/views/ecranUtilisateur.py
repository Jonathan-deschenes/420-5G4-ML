import customtkinter as ctk

from views.composants import (
    BLANC,
    GRIS_CLAIR,
    NOIR,
    TEXTE,
    VERT,
    BoutonRond,
    ModaleAjout,
    police,
)


UTILISATEURS_FICTIFS = [
    {"nom": "Marie Dubois", "identifiant": "USR001", "livre": "Les Misérables"},
    {"nom": "Jean Martin", "identifiant": "USR002", "livre": "Madame Bovary"},
    {"nom": "Sophie Lemaire", "identifiant": "USR003", "livre": ""},
    {"nom": "Pierre Durand", "identifiant": "USR004", "livre": "Germinal"},
    {"nom": "Claire Bernard", "identifiant": "USR005", "livre": ""},
    {"nom": "Marc Leroy", "identifiant": "USR006", "livre": "Les Fleurs du mal"},
    {"nom": "Anne Moreau", "identifiant": "USR007", "livre": ""},
    {"nom": "Alexandra Dumont", "identifiant": "USR015", "livre": ""},
]


class EcranUtilisateur(ctk.CTkFrame):
    def __init__(self, master, on_ajout=None):
        super().__init__(master, fg_color=BLANC, corner_radius=0)
        self.utilisateurs = [dict(utilisateur) for utilisateur in UTILISATEURS_FICTIFS]
        self.on_ajout = on_ajout

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._construire()
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

    def _afficher_lignes(self):
        for enfant in self.liste.winfo_children():
            enfant.destroy()

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

            if utilisateur["livre"]:
                actions = ctk.CTkFrame(ligne, fg_color=fond, corner_radius=0)
                actions.grid(row=0, column=1, sticky="e", padx=(0, 44))

                BoutonRond(
                    actions,
                    "retour",
                    lambda utilisateur_cible=utilisateur: self._rendre_livre(
                        utilisateur_cible
                    ),
                    fond=fond,
                    couleur_fond=NOIR,
                    couleur_survol="#2C2C2C",
                    taille=30,
                    taille_icone=16,
                ).pack(side="right")

                ctk.CTkLabel(
                    actions,
                    text=utilisateur["livre"],
                    width=240,
                    height=32,
                    corner_radius=16,
                    fg_color=VERT,
                    text_color=BLANC,
                    font=police(13),
                ).pack(side="right", padx=(0, 8))

    def _rendre_livre(self, utilisateur):
        utilisateur["livre"] = ""
        self._afficher_lignes()

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
        self.utilisateurs.append(
            {
                "nom": donnees["nom"],
                "identifiant": donnees["identifiant"],
                "livre": "",
            }
        )
        self._afficher_lignes()
        if self.on_ajout is not None:
            self.on_ajout()
