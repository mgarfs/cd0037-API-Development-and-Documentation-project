
# Changelog
Created this file.

## Install Dependencies
DONE beforehand. Note: Not using Virtual Environment.

## Set up Database
DID:
    sudo service postgresql start
    sudo -u postgres -i
        createdb trivia
    sudo -u postgres psql
        \c trivia
        \i trivia.psql
    updated `database_path` in models.py
    updated ../.gitignore to exclude `backend/models.py` (for security reasons)
        + cd ..
        + git update-index --skip-worktree backend/models.py

## Run the Server
DID:
    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run --reload
