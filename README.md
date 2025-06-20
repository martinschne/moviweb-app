# Moviweb App

Web application allowing users
to save their favorite movies from online movie database.

## Features:

- add user (rate limit 3 per day)
- add movie to the user
- add user note to the movie
- see all users
- see user's movie list
- see count of movies and users added

## Tech stack:

- Frontend:
    - CSS
    - Bulma
    - JavaScript
- Backend:
    - Python
    - Flask & Jinja2
- Database
    - SQL Alchemy
    - SQLite

## Usage

1. Run `project/setup.py` file. You will be asked if you want to populate the database with test data.
   For production skip this step by pressing `Enter`.
2. Change `Config` to `DevelopmentConfig` to activate development configuration in `app.py`.
3. Run `app.py` file.
4. Visit `localhost:5000` from your browser.


