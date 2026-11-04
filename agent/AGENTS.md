# AGENTS.md

## Build
- `cmake -S . -B build && cmake --build build` (README uses `mkdir build && cd build && cmake .. && make`).
- C++17, `-Wall -Wextra -Wpedantic`; binary is `build/bibliotheque`.
- `CMakeLists.txt` globs `*.cpp` without `CONFIGURE_DEPENDS`: after adding/removing a source file, re-run `cmake -S . -B build` — plain `make` will not pick it up.
- `build/` is gitignored (`agent/.gitignore`).

## Run
- From `agent/`: `./build/bibliotheque -d data`; from `build/`: `./bibliotheque -d ../data`.
- `-d/--data-dir` is effectively required: without it `FileManager` gets empty filenames, so no data is loaded or saved.
- `data/books.txt` and `data/users.txt` are test fixtures.

## Run GUI
- Windows: from `agent/GUI/`, launch with `py main.py` (no `.venv-win` required).
- If `customtkinter` is missing: `py -m pip install -r requirements.txt`.
- Headless check in the devcontainer: `cd agent/GUI && xvfb-run -a .venv/bin/python main.py`.

## Persistence formats
- `books.txt`: `title|author|isbn|1|borrowerId` (`1` available, `0` checked out).
- `users.txt`: `name|userId|isbn,isbn`.
- The app rewrites both files on menu “save” and on exit; backups append `.backup`.

## Architecture
- `main.cpp` is an interactive French CLI menu → `Library` owns `unique_ptr<Book>`/`User` → `FileManager` loads/saves the two text files.
- Standard library only (`<filesystem>` included); no tests, lint, CI, or third-party dependencies. Verify by building and exercising the menu.

## Conventions / gotchas
- UI strings and comments are French; keep new text French.
- Working tree is CRLF while HEAD is LF (no `.gitattributes`), so `git diff` shows whole-file churn — avoid committing line-ending-only changes.
- Existing commits use `[REMISE]` / `[SAUVEGARDE]` tags.
