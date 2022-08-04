
# Changelog
Created this file.

## INITIAL SETUP

### Installing Dependencies
Node and NPM DONE beforehand.
DID:
```
    npm install
```

### Running Your Frontend
DID:    
```
    npm start
```
RESULT:
```
    Unable to load questions. Please try your request again
    ("GET /questions?page=1 HTTP/1.1" 404 -)
```

## FIRST APP ROUTE
No changes.

## SECOND APP ROUTE

### QuestionView
DID in `QuestionView.js`:
```
    updated getQuestions to match actual json retrieved for totalQuestions and currentCategory
```

### Testing
Started the application and saw questions and categories generated, ten questions per page and pagination at the bottom of the screen for two pages. Clicking on the page numbers updates the questions.
