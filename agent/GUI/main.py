import customtkinter as ctk


MODES = {
    "Clair": "Light",
    "Sombre": "Dark",
    "Système": "System",
}


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.title("Bibliothèque - Test GUI")
        self.geometry("520x360")
        self.minsize(420, 300)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        conteneur = ctk.CTkFrame(self, corner_radius=16)
        conteneur.grid(row=0, column=0, padx=24, pady=24, sticky="nsew")
        conteneur.grid_columnconfigure(0, weight=1)

        titre = ctk.CTkLabel(
            conteneur,
            text="Test CustomTkinter",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        titre.grid(row=0, column=0, padx=20, pady=(24, 8))

        sous_titre = ctk.CTkLabel(
            conteneur,
            text="Entre ton nom puis clique sur Valider.",
            text_color=("gray30", "gray70"),
        )
        sous_titre.grid(row=1, column=0, padx=20, pady=(0, 20))

        self.entree = ctk.CTkEntry(conteneur, placeholder_text="Ton nom")
        self.entree.grid(row=2, column=0, padx=20, pady=(0, 12), sticky="ew")
        self.entree.bind("<Return>", lambda _event: self.valider())

        self.bouton = ctk.CTkButton(conteneur, text="Valider", command=self.valider)
        self.bouton.grid(row=3, column=0, padx=20, pady=(0, 12))

        self.resultat = ctk.CTkLabel(conteneur, text="")
        self.resultat.grid(row=4, column=0, padx=20, pady=(0, 16))

        self.mode = ctk.CTkSegmentedButton(
            conteneur, values=list(MODES), command=self.changer_mode
        )
        self.mode.set("Système")
        self.mode.grid(row=5, column=0, padx=20, pady=(0, 24))

        self.entree.focus_set()

    def valider(self):
        nom = self.entree.get().strip()
        if nom:
            self.resultat.configure(
                text=f"Bonjour, {nom} !", text_color=("gray10", "gray90")
            )
        else:
            self.resultat.configure(
                text="Veuillez entrer un nom.", text_color=("red", "salmon")
            )

    def changer_mode(self, valeur):
        ctk.set_appearance_mode(MODES[valeur])


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
