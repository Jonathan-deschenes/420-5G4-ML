cmake_minimum_required(VERSION 3.18)
project(bibliotheque_core LANGUAGES CXX)

set(PYBIND11_FINDPYTHON ON)
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(bibliotheque_core
    bindings.cpp
    ../../book.cpp
    ../../user.cpp
    ../../library.cpp
    ../../filemanager.cpp
)

target_include_directories(bibliotheque_core PRIVATE ../..)

set_target_properties(bibliotheque_core PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED YES
    CXX_EXTENSIONS NO
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
)

if(MSVC)
    target_compile_options(bibliotheque_core PRIVATE /W4)
else()
    target_compile_options(bibliotheque_core PRIVATE -Wall -Wextra -Wpedantic)
endif()
