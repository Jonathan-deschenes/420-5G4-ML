import unicodedata

from models import User


def _normaliser(texte):
    return (
        unicodedata.normalize("NFKD", texte)
        .encode("ascii", "ignore")
        .decode("ascii")
        .casefold()
    )


class UtilisateurControleur:
    def __init__(self, bibliotheque, on_modification=None):
        self.bibliotheque = bibliotheque
        self.on_modification = on_modification

    def _livre_en_dict(self, isbn):
        livre = self.bibliotheque.find_book_by_isbn(isbn)
        titre = isbn if livre is None else livre.title
        return {"isbn": isbn, "titre": titre}

    def _en_dict(self, utilisateur):
        return {
            "nom": utilisateur.name,
            "identifiant": utilisateur.user_id,
            "livres": [
                self._livre_en_dict(isbn)
                for isbn in utilisateur.borrowed_books
            ],
        }

    def _notifier(self):
        if self.on_modification is not None:
            self.on_modification()

    def lister(self, recherche=None):
        utilisateurs = [
            self._en_dict(utilisateur)
            for utilisateur in self.bibliotheque.get_all_users()
        ]

        if recherche is not None and recherche.strip():
            terme = _normaliser(recherche.strip())
            utilisateurs = [
                utilisateur
                for utilisateur in utilisateurs
                if terme in _normaliser(utilisateur["nom"])
                or terme in _normaliser(utilisateur["identifiant"])
            ]

        return utilisateurs

    def obtenir(self, identifiant):
        utilisateur = self.bibliotheque.find_user_by_id(identifiant)
        if utilisateur is None:
            return None
        return self._en_dict(utilisateur)

    def ajouter(self, nom, identifiant):
        nom = (nom or "").strip()
        identifiant = (identifiant or "").strip()

        if not nom:
            raise ValueError("Le nom est obligatoire.")
        if not identifiant:
            raise ValueError("L'identifiant utilisateur est obligatoire.")
        if self.bibliotheque.find_user_by_id(identifiant) is not None:
            raise ValueError(
                f"Un utilisateur avec l'identifiant {identifiant} existe déjà."
            )

        self.bibliotheque.add_user(User(nom, identifiant))
        self._notifier()
        return self.obtenir(identifiant)

    def livres_empruntes(self, identifiant):
        utilisateur = self.bibliotheque.find_user_by_id(identifiant)
        if utilisateur is None:
            return []
        return [
            self._livre_en_dict(isbn)
            for isbn in utilisateur.borrowed_books
        ]

    def retourner_livre(self, identifiant, isbn):
        utilisateur = self.bibliotheque.find_user_by_id(identifiant)
        if utilisateur is None or not utilisateur.has_borrowed_book(isbn):
            return False

        succes = self.bibliotheque.return_book(isbn)
        if succes:
            self._notifier()
        return succes
