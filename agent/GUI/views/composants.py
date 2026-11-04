import math
import tkinter as tk

import customtkinter as ctk


BLANC = "#FFFFFF"
NOIR = "#0B0B0B"
TEXTE = "#171717"
GRIS = "#7B7B7B"
GRIS_FONCE = "#3F3F3F"
GRIS_CLAIR = "#F2F2F2"
GRIS_SURVOL = "#E7E7E7"
BORDURE = "#DADADA"
ORANGE = "#F4B26E"
VERT = "#7CB46E"
VERT_SURVOL = "#6AA25C"
ROUGE = "#D92D20"
ROUGE_SURVOL = "#B42318"
FOND_CHAMP = "#F5F5F5"
POLICE = "Segoe UI"


def police(taille, poids="normal"):
    return ctk.CTkFont(family=POLICE, size=taille, weight=poids)


def dessiner_icone(canvas, nom, taille, couleur, ox=0, oy=0, epaisseur=None):
    def x(valeur):
        return ox + valeur * taille

    def y(valeur):
        return oy + valeur * taille

    trait = epaisseur if epaisseur is not None else max(1.4, taille * 0.085)
    options = {
        "fill": couleur,
        "width": trait,
        "capstyle": tk.ROUND,
        "joinstyle": tk.ROUND,
    }

    if nom == "recherche":
        canvas.create_oval(x(0.18), y(0.18), x(0.64), y(0.64), outline=couleur, width=trait)
        canvas.create_line(x(0.58), y(0.58), x(0.84), y(0.84), **options)
    elif nom == "fermer":
        canvas.create_line(x(0.25), y(0.25), x(0.75), y(0.75), **options)
        canvas.create_line(x(0.75), y(0.25), x(0.25), y(0.75), **options)
    elif nom == "livre":
        canvas.create_line(x(0.5), y(0.2), x(0.5), y(0.82), **options)
        canvas.create_line(
            x(0.5), y(0.2), x(0.18), y(0.14), x(0.18), y(0.72), x(0.5), y(0.82), **options
        )
        canvas.create_line(
            x(0.5), y(0.2), x(0.82), y(0.14), x(0.82), y(0.72), x(0.5), y(0.82), **options
        )
    elif nom == "utilisateur":
        canvas.create_oval(x(0.37), y(0.18), x(0.63), y(0.44), outline=couleur, width=trait)
        canvas.create_arc(
            x(0.18),
            y(0.52),
            x(0.82),
            y(1.08),
            start=0,
            extent=180,
            style=tk.ARC,
            outline=couleur,
            width=trait,
        )
    elif nom == "filtre":
        canvas.create_line(x(0.18), y(0.3), x(0.82), y(0.3), **options)
        canvas.create_line(x(0.28), y(0.5), x(0.72), y(0.5), **options)
        canvas.create_line(x(0.38), y(0.7), x(0.62), y(0.7), **options)
    elif nom == "retour":
        canvas.create_arc(
            x(0.18),
            y(0.18),
            x(0.82),
            y(0.82),
            start=35,
            extent=270,
            style=tk.ARC,
            outline=couleur,
            width=trait,
        )
        angle = math.radians(35)
        pointe_x = 0.5 + 0.32 * math.cos(angle)
        pointe_y = 0.5 - 0.32 * math.sin(angle)
        canvas.create_line(
            x(pointe_x),
            y(pointe_y),
            x(pointe_x - 0.13),
            y(pointe_y - 0.01),
            **options,
        )
        canvas.create_line(
            x(pointe_x),
            y(pointe_y),
            x(pointe_x - 0.01),
            y(pointe_y + 0.13),
            **options,
        )
    elif nom == "corbeille":
        canvas.create_line(x(0.18), y(0.28), x(0.82), y(0.28), **options)
        canvas.create_line(x(0.4), y(0.2), x(0.6), y(0.2), **options)
        canvas.create_polygon(
            x(0.3),
            y(0.32),
            x(0.7),
            y(0.32),
            x(0.64),
            y(0.83),
            x(0.36),
            y(0.83),
            outline=couleur,
            fill="",
            width=trait,
            joinstyle=tk.ROUND,
        )
        canvas.create_line(x(0.44), y(0.42), x(0.46), y(0.72), **options)
        canvas.create_line(x(0.56), y(0.42), x(0.54), y(0.72), **options)


class Icone(tk.Canvas):
    def __init__(self, parent, nom, taille=20, couleur=NOIR, fond=BLANC):
        super().__init__(
            parent,
            width=taille,
            height=taille,
            bg=fond,
            highlightthickness=0,
            bd=0,
        )
        self.nom = nom
        self.taille = taille
        self.couleur = couleur
        self.redessiner()

    def redessiner(self):
        self.delete("all")
        dessiner_icone(self, self.nom, self.taille, self.couleur)

    def configurer(self, couleur=None, fond=None):
        if fond is not None:
            self.configure(bg=fond)
        if couleur is not None:
            self.couleur = couleur
        self.redessiner()


class BoutonRond(tk.Canvas):
    def __init__(
        self,
        parent,
        nom_icone,
        commande,
        fond=BLANC,
        couleur_fond=NOIR,
        couleur_survol="#2C2C2C",
        couleur_icone=BLANC,
        taille=30,
        taille_icone=15,
    ):
        super().__init__(
            parent,
            width=taille,
            height=taille,
            bg=fond,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )
        self.commande = commande
        self.couleur_fond = couleur_fond
        self.couleur_survol = couleur_survol
        self.ovale = self.create_oval(
            1,
            1,
            taille - 1,
            taille - 1,
            fill=couleur_fond,
            outline="",
        )
        marge = (taille - taille_icone) / 2
        dessiner_icone(self, nom_icone, taille_icone, couleur_icone, marge, marge)
        self.bind("<Button-1>", self._clic)
        self.bind("<Enter>", self._entrer)
        self.bind("<Leave>", self._sortir)

    def _clic(self, _event):
        self.commande()

    def _entrer(self, _event):
        self.itemconfigure(self.ovale, fill=self.couleur_survol)

    def _sortir(self, _event):
        self.itemconfigure(self.ovale, fill=self.couleur_fond)


class BoutonIconeSimple(tk.Canvas):
    def __init__(
        self,
        parent,
        nom_icone,
        commande,
        fond=BLANC,
        couleur=GRIS,
        couleur_survol=NOIR,
        taille=32,
        taille_icone=17,
    ):
        super().__init__(
            parent,
            width=taille,
            height=taille,
            bg=fond,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )
        self.nom_icone = nom_icone
        self.commande = commande
        self.fond = fond
        self.couleur = couleur
        self.couleur_survol = couleur_survol
        self.taille = taille
        self.taille_icone = taille_icone
        self.survol = False
        self._dessiner()
        self.bind("<Button-1>", self._clic)
        self.bind("<Enter>", self._entrer)
        self.bind("<Leave>", self._sortir)

    def _dessiner(self):
        self.delete("all")
        if self.survol:
            self.create_oval(
                1,
                1,
                self.taille - 1,
                self.taille - 1,
                fill=GRIS_CLAIR,
                outline="",
            )
        couleur = self.couleur_survol if self.survol else self.couleur
        marge = (self.taille - self.taille_icone) / 2
        dessiner_icone(
            self,
            self.nom_icone,
            self.taille_icone,
            couleur,
            marge,
            marge,
        )

    def _clic(self, _event):
        self.commande()

    def _entrer(self, _event):
        self.survol = True
        self._dessiner()

    def _sortir(self, _event):
        self.survol = False
        self._dessiner()


class BarreRecherche(ctk.CTkFrame):
    def __init__(self, master, placeholder):
        super().__init__(master, fg_color=BLANC, corner_radius=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.icone = Icone(self, "recherche", 24, NOIR, fond=BLANC)
        self.icone.grid(row=0, column=0, padx=(40, 32), pady=24)
        self.icone.bind("<Button-1>", lambda _event: self.entree.focus_set())

        self.entree = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            fg_color=BLANC,
            border_width=0,
            corner_radius=0,
            height=46,
            font=police(18),
            text_color=TEXTE,
            placeholder_text_color=GRIS,
        )
        self.entree.grid(row=0, column=1, sticky="ew", pady=14)

        self.bouton_effacer = BoutonIconeSimple(
            self,
            "fermer",
            self.effacer,
            fond=BLANC,
            couleur=GRIS_FONCE,
            couleur_survol=NOIR,
        )
        self.bouton_effacer.grid(row=0, column=2, padx=(12, 40), pady=18)

        self.ligne = ctk.CTkFrame(self, fg_color=BORDURE, width=1, height=1, corner_radius=0)
        self.ligne.grid(row=1, column=0, columnspan=3, sticky="ew")

    def definir_placeholder(self, texte):
        self.entree.configure(placeholder_text=texte)

    def effacer(self):
        self.winfo_toplevel().focus_set()
        self.entree.delete(0, "end")
        self.entree.configure(
            placeholder_text=self.entree.cget("placeholder_text")
        )


class Onglet(ctk.CTkFrame):
    def __init__(self, master, texte, nom_icone, commande):
        super().__init__(master, fg_color=BLANC, corner_radius=0)
        self.commande = commande
        self.grid_columnconfigure(0, weight=1)

        self.contenu = ctk.CTkFrame(self, fg_color=BLANC, corner_radius=0)
        self.contenu.grid(row=0, column=0, sticky="w")

        self.icone = Icone(self.contenu, nom_icone, 22, GRIS, fond=BLANC)
        self.icone.grid(row=0, column=0, padx=(0, 10))

        self.police_active = police(16, "bold")
        self.police_inactive = police(16, "normal")
        self.label = ctk.CTkLabel(
            self.contenu,
            text=texte,
            font=self.police_inactive,
            text_color=GRIS,
        )
        self.label.grid(row=0, column=1)

        self.soulignement = ctk.CTkFrame(
            self,
            fg_color=BLANC,
            width=1,
            height=3,
            corner_radius=0,
        )
        self.soulignement.grid(row=1, column=0, sticky="ew", pady=(10, 0))

        for widget in (self, self.contenu, self.icone, self.label):
            widget.bind("<Button-1>", self._clic)

    def _clic(self, _event):
        self.commande()

    def definir_actif(self, actif):
        couleur = NOIR if actif else GRIS
        self.label.configure(
            text_color=couleur,
            font=self.police_active if actif else self.police_inactive,
        )
        self.icone.configurer(couleur=couleur)
        self.soulignement.configure(fg_color=NOIR if actif else BLANC)


class BarreOnglets(ctk.CTkFrame):
    def __init__(self, master, commande):
        super().__init__(master, fg_color=BLANC, corner_radius=0)
        self.grid_columnconfigure(2, weight=1)

        self.onglet_livres = Onglet(
            self,
            "Livres",
            "livre",
            lambda: commande("livres"),
        )
        self.onglet_livres.grid(row=0, column=0, padx=(44, 36), pady=(14, 0), sticky="w")

        self.onglet_utilisateurs = Onglet(
            self,
            "Utilisateurs",
            "utilisateur",
            lambda: commande("utilisateurs"),
        )
        self.onglet_utilisateurs.grid(
            row=0,
            column=1,
            padx=(0, 44),
            pady=(14, 0),
            sticky="w",
        )

        self.ligne = ctk.CTkFrame(self, fg_color=BORDURE, width=1, height=1, corner_radius=0)
        self.ligne.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(10, 0))

    def definir_actif(self, nom):
        self.onglet_livres.definir_actif(nom == "livres")
        self.onglet_utilisateurs.definir_actif(nom == "utilisateurs")


class MenuFiltre(ctk.CTkFrame):
    LARGEUR = 220
    HAUTEUR_OPTION = 38
    MARGE = 4

    def __init__(self, master, options, selection, commande):
        hauteur = len(options) * self.HAUTEUR_OPTION + self.MARGE * 2
        super().__init__(
            master,
            width=self.LARGEUR,
            height=hauteur,
            fg_color=BLANC,
            border_width=1,
            border_color=BORDURE,
            corner_radius=4,
        )
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        for index, option in enumerate(options):
            bouton = ctk.CTkButton(
                self,
                text=option,
                anchor="w",
                height=self.HAUTEUR_OPTION - 4,
                corner_radius=0,
                fg_color=GRIS_CLAIR if option == selection else BLANC,
                hover_color=GRIS_CLAIR,
                text_color=TEXTE,
                font=police(14),
                command=lambda valeur=option: commande(valeur),
            )
            bouton.grid(
                row=index,
                column=0,
                sticky="ew",
                padx=self.MARGE,
                pady=(self.MARGE if index == 0 else 2, self.MARGE if index == len(options) - 1 else 2),
            )

    @property
    def hauteur(self):
        return len(self.grid_slaves()) * self.HAUTEUR_OPTION + self.MARGE * 2


class ModaleAjout(ctk.CTkToplevel):
    def __init__(self, parent, titre, champs, on_valider):
        super().__init__(parent, fg_color=BORDURE)
        self.parent = parent
        self.on_valider = on_valider
        self.champs = champs
        self.entrees = {}
        self.withdraw()
        self.overrideredirect(True)
        self.transient(parent)
        self.resizable(False, False)

        cadre = ctk.CTkFrame(self, fg_color=BLANC, corner_radius=0)
        cadre.pack(fill="both", expand=True, padx=1, pady=1)

        entete = ctk.CTkFrame(cadre, fg_color=BLANC, corner_radius=0)
        entete.pack(fill="x", padx=28, pady=(24, 12))
        entete.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            entete,
            text=titre,
            font=police(22, "bold"),
            text_color=TEXTE,
            anchor="w",
        ).grid(row=0, column=0, sticky="w")

        BoutonIconeSimple(
            entete,
            "fermer",
            self.fermer,
            fond=BLANC,
            couleur=GRIS,
            couleur_survol=NOIR,
        ).grid(row=0, column=1, sticky="e")

        formulaire = ctk.CTkFrame(cadre, fg_color=BLANC, corner_radius=0)
        formulaire.pack(fill="both", expand=True, padx=28)

        for cle, label, placeholder in champs:
            ctk.CTkLabel(
                formulaire,
                text=label,
                font=police(12),
                text_color=GRIS_FONCE,
                anchor="w",
            ).pack(fill="x", pady=(0, 6))

            entree = ctk.CTkEntry(
                formulaire,
                placeholder_text=placeholder,
                height=42,
                corner_radius=8,
                fg_color=FOND_CHAMP,
                border_width=0,
                font=police(14),
                text_color=TEXTE,
                placeholder_text_color=GRIS,
            )
            entree.pack(fill="x", pady=(0, 14))
            entree.bind("<KeyRelease>", lambda _event, e=entree: e.configure(border_width=0))
            self.entrees[cle] = entree

        actions = ctk.CTkFrame(cadre, fg_color=BLANC, corner_radius=0)
        actions.pack(fill="x", padx=28, pady=(8, 24))
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            actions,
            text="Annuler",
            command=self.fermer,
            height=42,
            corner_radius=21,
            fg_color=GRIS_CLAIR,
            hover_color=GRIS_SURVOL,
            text_color=TEXTE,
            font=police(14),
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))

        ctk.CTkButton(
            actions,
            text="Ajouter",
            command=self.valider,
            height=42,
            corner_radius=21,
            fg_color=NOIR,
            hover_color="#2C2C2C",
            text_color=BLANC,
            font=police(14),
        ).grid(row=0, column=1, sticky="ew", padx=(8, 0))

        self.bind("<Escape>", lambda _event: self.fermer())
        self.bind("<Return>", lambda _event: self.valider())

        self.update_idletasks()
        largeur = 460
        hauteur = max(320, self.winfo_reqheight())
        x = parent.winfo_rootx() + (parent.winfo_width() - largeur) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - hauteur) // 2
        self.geometry(f"{largeur}x{hauteur}+{x}+{y}")
        self.deiconify()
        self.lift()
        self.after(30, self._activer)

    def _activer(self):
        try:
            self.grab_set()
        except tk.TclError:
            pass
        self.focus_force()
        if self.entrees:
            premier = next(iter(self.entrees.values()))
            premier.focus_set()

    def valider(self):
        for entree in self.entrees.values():
            if not entree.get().strip():
                entree.configure(border_width=1, border_color=ROUGE)
                entree.focus_set()
                return

        donnees = {
            cle: entree.get().strip()
            for cle, entree in self.entrees.items()
        }
        self.on_valider(donnees)
        self.fermer()

    def fermer(self):
        try:
            self.grab_release()
        except tk.TclError:
            pass
        self.destroy()
