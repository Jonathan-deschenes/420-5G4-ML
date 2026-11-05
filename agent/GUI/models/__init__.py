try:
    from .bibliotheque_core import Book, FileManager, Library, User
except ImportError as erreur:
    raise ImportError(
        "Le module natif 'models.bibliotheque_core' est introuvable. "
        "Compilez-le avec CMake et pybind11 (voir GUI/models/CMakeLists.txt)."
    ) from erreur

__all__ = ["Book", "FileManager", "Library", "User"]
