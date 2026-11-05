import unicodedata

from models import Book


def _normaliser(texte):
    return (
        unicodedata.normalize("NFKD", texte)
        .encode("ascii", "ignore")
        .decode("ascii")
        .casefold()
    )


class LivreControleur:
    def __init__(self, bibliotheque, on_modification=None):
        self.bibliotheque = bibliotheque
        self.on_modification = on_modification

    def _en_dict(self, livre):
        return {
            "titre": livre.title,
            "auteur": livre.author,
            "isbn": livre.isbn,
            "disponible": livre.is_available,
            "id_emprunteur": livre.borrower_id,
        }

    def _notifier(self):
        if self.on_modification is not None:
            self.on_modification()

    def _valider(self, titre, auteur, isbn):
        titre = (titre or "").strip()
        auteur = (auteur or "").strip()
        isbn = (isbn or "").strip()

        if not titre:
            raise ValueError("Le titre est obligatoire.")
        if not auteur:
            raise ValueError("L'auteur est obligatoire.")
        if not isbn:
            raise ValueError("L'ISBN est obligatoire.")

        return titre, auteur, isbn

    def lister(self, disponibles_seulement=False, recherche=None):
        if recherche is not None and recherche.strip():
            livres = self.rechercher(recherche)
        else:
            if disponibles_seulement:
                source = self.bibliotheque.get_available_books()
            else:
                source = self.bibliotheque.get_all_books()
            livres = [self._en_dict(livre) for livre in source]

        if disponibles_seulement:
            livres = [livre for livre in livres if livre["disponible"]]

        return livres

    def rechercher(self, texte):
        texte = (texte or "").strip()
        if not texte:
            return self.lister()

        minuscule = _normaliser(texte)
        trouves = {}
        for livre in self.bibliotheque.get_all_books():
            if (
                minuscule in _normaliser(livre.title)
                or minuscule in _normaliser(livre.author)
                or minuscule in _normaliser(livre.isbn)
            ):
                trouves[livre.isbn] = livre

        return [self._en_dict(livre) for livre in trouves.values()]

    def obtenir(self, isbn):
        livre = self.bibliotheque.find_book_by_isbn(isbn)
        if livre is None:
            return None
        return self._en_dict(livre)

    def ajouter(self, titre, auteur, isbn):
        titre, auteur, isbn = self._valider(titre, auteur, isbn)

        if self.bibliotheque.find_book_by_isbn(isbn) is not None:
            raise ValueError(f"Un livre avec l'ISBN {isbn} existe déjà.")

        self.bibliotheque.add_book(Book(titre, auteur, isbn))
        self._notifier()
        return self.obtenir(isbn)

    def supprimer(self, isbn):
        if self.bibliotheque.find_book_by_isbn(isbn) is None:
            return False

        for utilisateur in self.bibliotheque.get_all_users():
            if utilisateur.has_borrowed_book(isbn):
                utilisateur.return_book(isbn)

        succes = self.bibliotheque.remove_book(isbn)
        if succes:
            self._notifier()
        return succes

    def emprunter(self, isbn, id_utilisateur):
        succes = self.bibliotheque.check_out_book(isbn, id_utilisateur)
        if succes:
            self._notifier()
        return succes

    def retourner(self, isbn):
        succes = self.bibliotheque.return_book(isbn)
        if succes:
            self._notifier()
        return succes
