import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, questions):
    page = request.args.get("page", 1, type=int)
    start_page_question = (page - 1) * QUESTIONS_PER_PAGE
    end_page_question = start_page_question + QUESTIONS_PER_PAGE

    all_questions = [question.format() for question in questions]
    page_questions = all_questions[start_page_question:end_page_question]

    return page_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False # we decide the order
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,DELETE" # consider including PUT and OPTIONS
        )
        return response

    @app.route("/categories")
    def retrieve_categories():
        """
        Endpoint to handle GET requests for all available categories.
        GET '/categories'
        {
          'categories': { 
            '1' : "Science",
            '2' : "Art",
            '3' : "Geography",
            '4' : "History",
            '5' : "Entertainment",
            '6' : "Sports"
          }
        }
        """
        categories = Category.query.order_by(Category.id).all()
        data={}
        for category in categories:
            data[category.id]=category.type
        if len(data) == 0:
            abort(404)
        else:
            return jsonify(
                {
                    "categories": data,
                }
            )

    @app.route("/questions")
    def retrieve_questions():
        """
        Endpoint to handle GET requests for questions, including pagination (every 10 questions).
        This endpoint returns a list of questions, number of total questions, current category, categories.
        GET '/questions?page=${integer}'
        {
          'questions': [
            {
              'id': 1,
              'question': 'This is a question',
              'answer': 'This is an answer',
              'difficulty': 5,
              'category': 2
            },
            ...
          ],
          'totalQuestions': 100,
          'categories': { 
            '1' : "Science",
            ...
          },
          'currentCategory': 'History'
        }
        """
        questions = Question.query.order_by(Question.category).order_by(Question.id).all()
        page_questions = paginate_questions(request, questions)
        if len(page_questions) == 0:
            abort(404)
        else:
            categories = Category.query.order_by(Category.id).all()
            category_data={}
            for category in categories:
                category_data[category.id]=category.type

            return jsonify(
                {
                    "questions": page_questions,
                    "totalQuestions": len(Question.query.all()),
                    "categories": category_data,
                    "currentCategory": category_data[int(page_questions[-1:][0]['category'])]
                }
            )

    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_question(question_id):
        """
        Create an endpoint to DELETE question using a question ID.
        This removal will persist in the database and when you refresh the page.

        - Deletes a specified question using the id of the question
        - Request Arguments: id - integer
        - Returns: Does not need to return anything besides the appropriate HTTP status code. @TODO: Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.
        DELETE '/questions/${id}'
        """
        try:
            question=Question.query.filter(Question.id==question_id).one_or_none()
            if question is None:
                abort(404)
            else:
                question.delete()
                return (jsonify({"success": True}), 200)
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/categories/<category_id>/questions')
    def retrieve_category_questions(category_id):
        """
        Endpoint to get questions based on category.


        - Fetches questions for a cateogry specified by id request argument
        - Request Arguments: id - integer
        - Returns: An object with questions for the specified category, total questions, and current category string
        GET '/categories/${id}/questions'
        {
          'questions': [
            {
              'id': 1,
              'question': 'This is a question',
              'answer': 'This is an answer',
              'difficulty': 5,
              'category': 4
            },
            ...
          ],
          'totalQuestions': 100,
          'currentCategory': 'History'
        }
        """
        category=Category.query.filter(Category.id==int(category_id)).one_or_none()
        if category is None:
            abort(404)
        else:
            questions=Question.query.filter(Question.category==category_id).order_by(Question.id).all()
            all_questions = [question.format() for question in questions]
            return jsonify(
                {
                    "questions": all_questions,
                    "totalQuestions": len(Question.query.all()),
                    "currentCategory": category.type
                }
            )

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    Error handlers for all expected errors - including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Resource not found"}),
            404
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "Unable to process request"}),
            422
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "Bad request"}), 
            400
        )

    return app

