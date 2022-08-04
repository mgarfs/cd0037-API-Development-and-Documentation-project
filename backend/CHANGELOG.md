
# Changelog
Created this file.

## INITIAL SETUP

### Install Dependencies
DONE beforehand. Note: Not using Virtual Environment.

### Set up Database
DID:
```bash
    sudo service postgresql start
    sudo -u postgres -i
        createdb trivia
    sudo -u postgres psql
        \c trivia
        \i trivia.psql
```
DID:
```
    updated `database_path` in models.py
    updated ../.gitignore to exclude `backend/models.py` (for security reasons)
        + cd ..
        + git update-index --skip-worktree backend/models.py
```

### Run the Server
DID:
```bash
    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run --reload
```

### Tried Testing
DID:
```bash
    python3 test_flaskr.py
```

## FIRST APP ROUTE WITH TESTING

### Implemented app route = GET /categories
DID updates to `__init__.py`:
```
    CORS(app)
    @app.after_request
    @app.route("/categories")
```

### Set up Test Database
DID:
```bash
    sudo -u postgres -i
        createdb trivia_test
    sudo -u postgres psql
        \c trivia_test
        \i trivia.psql
```

### Implemented test for GET /categories
DID updates to `test_flaskr.py`:
```
    updated `database_path`
    test_retrieve_categories
```
DID:
```bash
    python3 -W ignore::DeprecationWarning test_flaskr.py
```
RESULT:
```
.
----------------------------------------------------------------------
Ran 1 test in 0.037s

OK
```

### Updated bakend/README.md
DID:
    Documenting your Endpoints
    Testing (note about deprecation warnings)

## SECOND APP ROUTE

### Implemented app route = GET /questions?page=#
DID updates to `__init__.py`:
```
    app.config['JSON_SORT_KEYS'] = False # we decide the order
    def paginate_questions(request, questions)
    @app.route("/questions")
```
DID updates to `test_flaskr.py`:
```
    test_retrieve_questions
```

## REMAINING APP ROUTES

### Testing
Created `re_insert_questions.sql` for re-establishing deleted questions as part of testing!