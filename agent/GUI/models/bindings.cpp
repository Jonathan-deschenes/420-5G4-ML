#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "book.h"
#include "library.h"
#include "user.h"

namespace py = pybind11;

PYBIND11_MODULE(bibliotheque_core, m) {
    m.doc() = "Liaison pybind11 entre la GUI Python et la bibliothèque C++";

    py::class_<Book>(m, "Book")
        .def(py::init<>())
        .def(py::init<const std::string&, const std::string&, const std::string&>(),
             py::arg("title"), py::arg("author"), py::arg("isbn"))
        .def_property("title", &Book::getTitle, &Book::setTitle)
        .def_property("author", &Book::getAuthor, &Book::setAuthor)
        .def_property("isbn", &Book::getISBN, &Book::setISBN)
        .def_property("is_available", &Book::getAvailability, &Book::setAvailability)
        .def_property("borrower_id", &Book::getBorrowerId, &Book::setBorrowerId)
        .def("check_out", &Book::checkOut, py::arg("borrower_id"))
        .def("return_book", &Book::returnBook)
        .def("to_string", &Book::toString)
        .def("to_file_format", &Book::toFileFormat)
        .def("from_file_format", &Book::fromFileFormat, py::arg("line"))
        .def("__str__", &Book::toString)
        .def("__repr__", [](const Book& book) {
            return "Book(title='" + book.getTitle() + "', isbn='" + book.getISBN() + "')";
        });

    py::class_<User>(m, "User")
        .def(py::init<>())
        .def(py::init<const std::string&, const std::string&>(),
             py::arg("name"), py::arg("user_id"))
        .def_property("name", &User::getName, &User::setName)
        .def_property("user_id", &User::getUserId, &User::setUserId)
        .def_property_readonly("borrowed_books", &User::getBorrowedBooks)
        .def("borrow_book", &User::borrowBook, py::arg("isbn"))
        .def("return_book", &User::returnBook, py::arg("isbn"))
        .def("has_borrowed_book", &User::hasBorrowedBook, py::arg("isbn"))
        .def("get_number_of_borrowed_books", &User::getNumberOfBorrowedBooks)
        .def("to_string", &User::toString)
        .def("to_file_format", &User::toFileFormat)
        .def("from_file_format", &User::fromFileFormat, py::arg("line"))
        .def("__str__", &User::toString)
        .def("__repr__", [](const User& user) {
            return "User(name='" + user.getName() + "', user_id='" + user.getUserId() + "')";
        });

    py::class_<Library>(m, "Library")
        .def(py::init<>())
        .def("add_book", &Library::addBook, py::arg("book"))
        .def("remove_book", &Library::removeBook, py::arg("isbn"))
        .def("find_book_by_isbn", &Library::findBookByISBN, py::arg("isbn"),
             py::return_value_policy::reference_internal)
        .def("search_books_by_title", &Library::searchBooksByTitle, py::arg("title"),
             py::return_value_policy::reference_internal)
        .def("search_books_by_author", &Library::searchBooksByAuthor, py::arg("author"),
             py::return_value_policy::reference_internal)
        .def("get_available_books", &Library::getAvailableBooks,
             py::return_value_policy::reference_internal)
        .def("get_all_books", &Library::getAllBooks,
             py::return_value_policy::reference_internal)
        .def("add_user", &Library::addUser, py::arg("user"))
        .def("find_user_by_id", &Library::findUserById, py::arg("user_id"),
             py::return_value_policy::reference_internal)
        .def("get_all_users", &Library::getAllUsers,
             py::return_value_policy::reference_internal)
        .def("check_out_book", &Library::checkOutBook, py::arg("isbn"), py::arg("user_id"))
        .def("return_book", &Library::returnBook, py::arg("isbn"))
        .def("get_total_books", &Library::getTotalBooks)
        .def("get_available_book_count", &Library::getAvailableBookCount)
        .def("get_checked_out_book_count", &Library::getCheckedOutBookCount)
        .def("__repr__", [](const Library& library) {
            return "Library(total_books=" + std::to_string(library.getTotalBooks()) +
                   ", available_books=" + std::to_string(library.getAvailableBookCount()) + ")";
        });
}
