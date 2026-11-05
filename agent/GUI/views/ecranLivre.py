import customtkinter as ctk

from views.composants import (
    BLANC,
    GRIS,
    GRIS_CLAIR,
    NOIR,
    ORANGE,
    ROUGE,
    ROUGE_SURVOL,
    TEXTE,
    BoutonRond,
    Icone,
    MenuFiltre,
    ModaleAjout,
    ModaleSelection,
    afficher_erreur,
    police,
)


class EcranLivre(ctk.CTkFrame):
    def __init__(self, master, bibliotheque):
        super().__init__(master, fg_color=BLANC, corner_radius=0)
        self.bibliotheque = bibliotheque
        self.livres = []
        self.statistiques = {
            "total": 0,
            "disponibles": 0,
            "empruntes": 0,
            "utilisateurs": 0,
        }
        self.filtre = "Tous les livres"
        self.recherche = ""
        self.menu_filtre = None
        self.id_clic_exterieur = None
        self.id_echap = None
        self.labels_statistiques = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._construire()
        self._charger_donnees()
        self._afficher_lignes()

    def _construire(self):
        statistiques = ctk.CTkFrame(self, fg_color=BLANC, corner_radius=0)
        statistiques.grid(row=0, column=0, sticky="ew", padx=(70, 44), pady=(13, 10))
        for colonne in range(4):
            statistiques.grid_columnconfigure(colonne, weight=1)

        blocs = [
            ("total", "Total des livres"),
            ("disponibles", "Livres disponibles"),
            ("empruntes", "Livres empruntés"),
            ("utilisateurs", "Utilisateurs"),
        ]

        for colonne, (cle, libelle) in enumerate(blocs):
            bloc = ctk.CTkFrame(statistiques, fg_color=BLANC, corner_radius=0)
            bloc.grid(row=0, column=colonne, sticky="w")

            nombre = ctk.CTkLabel(
                bloc,
                text=str(self.statistiques[cle]),
                font=police(36),
                text_color=TEXTE,
                anchor="w",
            )
            nombre.grid(row=0, column=0, sticky="w")

            ctk.CTkLabel(
                bloc,
                text=libelle,
                font=police(11),
                text_color=GRIS,
                anchor="w",
            ).grid(row=1, column=0, sticky="w", pady=(2, 0))

            self.labels_statistiques[cle] = nombre

        actions = ctk.CTkFrame(self, fg_color=BLANC, corner_radius=0)
        actions.grid(row=1, column=0, sticky="ew", padx=44, pady=(12, 10))
        actions.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            actions,
            text="+  Ajouter livre",
            command=self.ouvrir_ajout,
            width=180,
            height=42,
            corner_radius=21,
            fg_color=NOIR,
            hover_color="#2C2C2C",
            text_color=BLANC,
            font=police(14),
        ).grid(row=0, column=0, sticky="w")

        self.zone_filtre = ctk.CTkFrame(actions, fg_color=BLANC, corner_radius=0)
        self.zone_filtre.grid(row=0, column=1, sticky="e")

        self.icone_filtre = Icone(
            self.zone_filtre,
            "filtre",
            18,
            GRIS,
            fond=BLANC,
        )
        self.icone_filtre.grid(row=0, column=0, padx=(0, 8))

        self.label_filtre = ctk.CTkLabel(
            self.zone_filtre,
            text="Filtrer",
            font=police(14),
            text_color=GRIS,
        )
        self.label_filtre.grid(row=0, column=1)

        for widget in (self.zone_filtre, self.icone_filtre, self.label_filtre):
            widget.bind("<Button-1>", lambda _event: self.ouvrir_filtre())
            widget.bind("<Enter>", lambda _event: self._survol_filtre(True))
            widget.bind("<Leave>", lambda _event: self._survol_filtre(False))

        self.liste = ctk.CTkScrollableFrame(
            self,
            fg_color=BLANC,
            corner_radius=0,
            scrollbar_fg_color=BLANC,
            scrollbar_button_color="#E4E4E4",
            scrollbar_button_hover_color="#CFCFCF",
        )
        self.liste.grid(row=2, column=0, sticky="nsew")
        self.liste.grid_columnconfigure(0, weight=1)

    def _survol_filtre(self, actif):
        couleur = NOIR if actif else GRIS
        self.label_filtre.configure(text_color=couleur)
        self.icone_filtre.configurer(couleur=couleur)

    def _maj_statistiques(self):
        for cle, label in self.labels_statistiques.items():
            label.configure(text=str(self.statistiques[cle]))

    def _charger_donnees(self):
        self.livres = self.bibliotheque.livres.lister(
            disponibles_seulement=self.filtre == "Seulement disponible",
            recherche=self.recherche,
        )
        self.statistiques = self.bibliotheque.statistiques()
        self._maj_statistiques()

    def rafraichir(self):
        self._charger_donnees()
        self._afficher_lignes()

    def rechercher(self, texte):
        self.recherche = texte
        self.rafraichir()

    def _afficher_lignes(self):
        for enfant in self.liste.winfo_children():
            enfant.destroy()

        livres = self.livres
        if not livres:
            ctk.CTkLabel(
                self.liste,
                text="Aucun livre à afficher",
                font=police(14),
                text_color=GRIS,
            ).grid(row=0, column=0, pady=40)
            return

        for index, livre in enumerate(livres):
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

            contenu = ctk.CTkFrame(ligne, fg_color=fond, corner_radius=0)
            contenu.grid(row=0, column=0, sticky="w", padx=(44, 0), pady=(5, 5))

            ctk.CTkLabel(
                contenu,
                text=livre["titre"],
                font=police(16),
                text_color=TEXTE,
                anchor="w",
                height=20,
            ).pack(anchor="w")

            ctk.CTkLabel(
                contenu,
                text=livre["auteur"],
                font=police(11),
                text_color=GRIS,
                anchor="w",
                height=16,
            ).pack(anchor="w", pady=(2, 0))

            ctk.CTkLabel(
                contenu,
                text=livre["isbn"],
                font=police(11),
                text_color=GRIS,
                anchor="w",
                height=16,
            ).pack(anchor="w", pady=(1, 0))

            actions = ctk.CTkFrame(ligne, fg_color=fond, corner_radius=0)
            actions.grid(row=0, column=1, sticky="e", padx=(0, 44))

            BoutonRond(
                actions,
                "corbeille",
                lambda livre_cible=livre: self._supprimer_livre(livre_cible),
                fond=fond,
                couleur_fond=ROUGE,
                couleur_survol=ROUGE_SURVOL,
                taille=30,
                taille_icone=15,
            ).pack(side="right")

            if livre["disponible"]:
                ctk.CTkButton(
                    actions,
                    text="Emprunter",
                    command=lambda livre_cible=livre: self._basculer_emprunt(livre_cible),
                    width=100,
                    height=32,
                    corner_radius=16,
                    fg_color=NOIR,
                    hover_color="#2C2C2C",
                    text_color=BLANC,
                    font=police(13),
                    bg_color=fond,
                ).pack(side="right", padx=(0, 14))
            else:
                BoutonRond(
                    actions,
                    "retour",
                    lambda livre_cible=livre: self._basculer_emprunt(livre_cible),
                    fond=fond,
                    couleur_fond=NOIR,
                    couleur_survol="#2C2C2C",
                    taille=30,
                    taille_icone=16,
                ).pack(side="right", padx=(0, 8))

                ctk.CTkLabel(
                    actions,
                    text="Indisponible",
                    width=100,
                    height=32,
                    corner_radius=16,
                    fg_color=ORANGE,
                    text_color=BLANC,
                    font=police(13),
                ).pack(side="right", padx=(0, 14))

    def _basculer_emprunt(self, livre):
        if livre["disponible"]:
            self._emprunter(livre)
        else:
            self._retourner(livre)

    def _emprunter(self, livre):
        utilisateurs = self.bibliotheque.utilisateurs.lister()
        if not utilisateurs:
            afficher_erreur(
                "Aucun utilisateur enregistré. Ajoutez un utilisateur "
                "avant d'emprunter un livre."
            )
            return

        options = [
            (
                utilisateur["identifiant"],
                f"{utilisateur['nom']} ({utilisateur['identifiant']})",
            )
            for utilisateur in utilisateurs
        ]
        ModaleSelection(
            self.winfo_toplevel(),
            "Choisir un utilisateur",
            options,
            lambda identifiant: self._confirmer_emprunt(livre, identifiant),
        )

    def _confirmer_emprunt(self, livre, identifiant):
        if not self.bibliotheque.livres.emprunter(livre["isbn"], identifiant):
            afficher_erreur(
                f"Impossible d'emprunter « {livre['titre']} » "
                f"pour {identifiant}."
            )

    def _retourner(self, livre):
        if not self.bibliotheque.livres.retourner(livre["isbn"]):
            afficher_erreur(
                f"Impossible de retourner « {livre['titre']} »."
            )

    def _supprimer_livre(self, livre):
        if not self.bibliotheque.livres.supprimer(livre["isbn"]):
            afficher_erreur(
                f"Impossible de supprimer « {livre['titre']} »."
            )

    def ouvrir_ajout(self):
        self.fermer_menu_filtre()
        champs = [
            ("titre", "Titre", "Ex. : Le Petit Prince"),
            ("auteur", "Auteur", "Ex. : Antoine de Saint-Exupéry"),
            ("isbn", "ISBN", "Ex. : 9782070612758"),
        ]
        ModaleAjout(
            self.winfo_toplevel(),
            "Ajouter un livre",
            champs,
            self._ajouter_livre,
        )

    def _ajouter_livre(self, donnees):
        try:
            self.bibliotheque.livres.ajouter(
                donnees["titre"],
                donnees["auteur"],
                donnees["isbn"],
            )
        except ValueError as erreur:
            afficher_erreur(str(erreur))
            return False
        return True

    def ouvrir_filtre(self):
        if self.menu_filtre is not None:
            self.fermer_menu_filtre()
            return

        self.menu_filtre = MenuFiltre(
            self,
            ["Tous les livres", "Seulement disponible"],
            self.filtre,
            self._choisir_filtre,
        )
        largeur = MenuFiltre.LARGEUR
        hauteur = self.menu_filtre.hauteur

        x = (
            self.zone_filtre.winfo_rootx()
            - self.winfo_rootx()
            + self.zone_filtre.winfo_width()
            - largeur
        )
        y = (
            self.zone_filtre.winfo_rooty()
            - self.winfo_rooty()
            + self.zone_filtre.winfo_height()
            + 4
        )
        x = max(8, min(x, max(8, self.winfo_width() - largeur - 8)))
        y = max(8, min(y, max(8, self.winfo_height() - hauteur - 8)))

        self.menu_filtre.place(x=x, y=y)
        self.menu_filtre.lift()

        racine = self.winfo_toplevel()
        self.id_clic_exterieur = racine.bind(
            "<Button-1>",
            self._clic_hors_menu,
            add="+",
        )
        self.id_echap = racine.bind(
            "<Escape>",
            lambda _event: self.fermer_menu_filtre(),
            add="+",
        )

    def _choisir_filtre(self, option):
        self.filtre = option
        self.fermer_menu_filtre()
        self.rafraichir()

    def _clic_hors_menu(self, event):
        if self.menu_filtre is None:
            return
        if self._est_descendant(event.widget, self.menu_filtre):
            return
        if self._est_descendant(event.widget, self.zone_filtre):
            return
        self.fermer_menu_filtre()

    @staticmethod
    def _est_descendant(widget, ancetre):
        while widget is not None:
            if widget == ancetre:
                return True
            widget = getattr(widget, "master", None)
        return False

    def fermer_menu_filtre(self):
        if self.menu_filtre is not None:
            self.menu_filtre.destroy()
            self.menu_filtre = None

        racine = self.winfo_toplevel()
        if self.id_clic_exterieur is not None:
            racine.unbind("<Button-1>", self.id_clic_exterieur)
            self.id_clic_exterieur = None
        if self.id_echap is not None:
            racine.unbind("<Escape>", self.id_echap)
            self.id_echap = None
