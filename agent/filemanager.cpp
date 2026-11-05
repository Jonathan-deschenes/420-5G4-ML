#include <fstream>
#include <iostream>
#include <filesystem>
#include <system_error>
#include "filemanager.h"

using namespace std;

namespace {

string stripCarriageReturn(const string& line) {
    if (!line.empty() && line.back() == '\r') {
        return line.substr(0, line.size() - 1);
    }
    return line;
}

string copyErrorMessage(const string& filename, const error_code& error) {
    return "Impossible de traiter " + filename + " : " + error.message();
}

}

// Constructor
FileManager::FileManager(const string& booksFile, const string& usersFile)
    : booksFileName(booksFile), usersFileName(usersFile) {}

bool FileManager::ensureParentDirectory(const string& filename) {
    const filesystem::path path(filename);
    const filesystem::path parent = path.parent_path();

    if (parent.empty()) {
        return true;
    }

    error_code error;
    if (!filesystem::exists(parent, error)) {
        if (!filesystem::create_directories(parent, error) && error) {
            lastError = copyErrorMessage(filename, error);
            return false;
        }
    } else if (error) {
        lastError = copyErrorMessage(filename, error);
        return false;
    }

    return true;
}

// Save all library data
bool FileManager::saveLibraryData(Library& library) {
    lastError.clear();
    const bool booksSaved = saveBooksToFile(library);
    const bool usersSaved = saveUsersToFile(library);
    return booksSaved && usersSaved;
}

// Load all library data
bool FileManager::loadLibraryData(Library& library) {
    lastError.clear();
    const bool booksLoaded = loadBooksFromFile(library);
    const bool usersLoaded = loadUsersFromFile(library);
    return booksLoaded || usersLoaded; // Return true if at least one file was loaded
}

// Save books to file
bool FileManager::saveBooksToFile(Library& library) {
    if (!ensureParentDirectory(booksFileName)) {
        return false;
    }

    ofstream file(booksFileName, ios::binary | ios::trunc);
    if (!file.is_open()) {
        lastError = "Impossible d'ouvrir " + booksFileName + " en écriture.";
        cout << "Erreur : " << lastError << "\n";
        return false;
    }

    for (Book* book : library.getAllBooks()) {
        file << book->toFileFormat() << "\n";
    }

    file.close();
    if (file.fail()) {
        lastError = "Impossible d'écrire dans " + booksFileName + ".";
        cout << "Erreur : " << lastError << "\n";
        return false;
    }

    return true;
}

// Save users to file
bool FileManager::saveUsersToFile(Library& library) {
    if (!ensureParentDirectory(usersFileName)) {
        return false;
    }

    ofstream file(usersFileName, ios::binary | ios::trunc);
    if (!file.is_open()) {
        lastError = "Impossible d'ouvrir " + usersFileName + " en écriture.";
        cout << "Erreur : " << lastError << "\n";
        return false;
    }

    for (User* user : library.getAllUsers()) {
        file << user->toFileFormat() << "\n";
    }

    file.close();
    if (file.fail()) {
        lastError = "Impossible d'écrire dans " + usersFileName + ".";
        cout << "Erreur : " << lastError << "\n";
        return false;
    }

    return true;
}

// Load books from file
bool FileManager::loadBooksFromFile(Library& library) {
    ifstream file(booksFileName, ios::binary);
    if (!file.is_open()) {
        cout << "Aucun fichier de livres existant trouvé. Démarrage avec une bibliothèque vide.\n";
        return false;
    }

    string line;
    int count = 0;
    while (getline(file, line)) {
        line = stripCarriageReturn(line);
        if (!line.empty()) {
            Book book;
            book.fromFileFormat(line);
            library.addBook(book);
            count++;
        }
    }

    if (file.bad()) {
        lastError = "Erreur de lecture dans " + booksFileName + ".";
        cout << "Erreur : " << lastError << "\n";
        return false;
    }

    file.close();
    cout << "Chargé " << count << " livre(s) depuis le fichier.\n";
    return true;
}

// Load users from file
bool FileManager::loadUsersFromFile(Library& library) {
    ifstream file(usersFileName, ios::binary);
    if (!file.is_open()) {
        cout << "Aucun fichier d'utilisateurs existant trouvé. Démarrage sans utilisateurs enregistrés.\n";
        return false;
    }

    string line;
    int count = 0;
    while (getline(file, line)) {
        line = stripCarriageReturn(line);
        if (!line.empty()) {
            User user;
            user.fromFileFormat(line);
            library.addUser(user);
            count++;
        }
    }

    if (file.bad()) {
        lastError = "Erreur de lecture dans " + usersFileName + ".";
        cout << "Erreur : " << lastError << "\n";
        return false;
    }

    file.close();
    cout << "Chargé " << count << " utilisateur(s) depuis le fichier.\n";
    return true;
}

// Check if file exists
bool FileManager::fileExists(const string& filename) {
    ifstream file(filename, ios::binary);
    return file.good();
}

// Create backup
bool FileManager::createBackup() {
    lastError.clear();
    bool success = true;

    for (const string& filename : {booksFileName, usersFileName}) {
        if (!filesystem::exists(filename)) {
            continue;
        }

        error_code error;
        filesystem::copy_file(
            filename,
            filename + ".backup",
            filesystem::copy_options::overwrite_existing,
            error
        );

        if (error) {
            lastError = copyErrorMessage(filename, error);
            cout << "Erreur : " << lastError << "\n";
            success = false;
        }
    }

    if (success) {
        cout << "Fichiers de sauvegarde créés.\n";
    }
    return success;
}

const string& FileManager::getBooksFileName() const {
    return booksFileName;
}

const string& FileManager::getUsersFileName() const {
    return usersFileName;
}

const string& FileManager::getLastError() const {
    return lastError;
}
