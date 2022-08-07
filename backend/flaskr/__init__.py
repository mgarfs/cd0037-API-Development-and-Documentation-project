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
    CORS(app)

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
        Endpoint to DELETE question using a question ID.
        Deletes a specified question using the id of the question
        Request Arguments: id - integer
        Returns: Does not need to return anything besides the appropriate HTTP status code.
        This removal will persist in the database and when you refresh the page.

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

    def create_question(question, answer, difficulty, category):
        """
        NB: Called from create_question_or_search_questions "shared" app route /questions - see below

        Endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
        Sends a post request in order to add a new question
        Returns: Does not return any new data

        POST '/questions'
        request body:
        {
            'question':  'Heres a new question string',
            'answer':  'Heres a new answer string',
            'difficulty': 1,
            'category': 3,
        }
        """
        try:
            question=Question(question, answer, category, difficulty)
            question.insert()
            return (jsonify({"success": True}), 200)
        except:
            abort(422)

    def search_questions(search_term, category):
        """
        NB: Called from create_question_or_search_questions "shared" app route /questions - see below

        Endpoint to get questions based on a search term via a POST.
        It returns any questions for whom the search term is a substring of the question.
        Sends a post request in order to search for a specific question by search term
        Returns: any array of questions, a number of totalQuestions that met the search term and the current category string
        
        POST '/questions'
        request body:
        {
            'searchTerm': 'this is the term the user is looking for'
        }
        reply:
        {
            'questions': [
                {
                    'id': 1,
                    'question': 'This is a question',
                    'answer': 'This is an answer',
                    'difficulty': 5,
                    'category': 5
                },
                ...
            ],
            'totalQuestions': 1,
            'currentCategory': 'Entertainment'
        }
        """
        questions=Question.query.order_by(Question.category).order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_term))).all()
        page_questions=paginate_questions(request, questions)
        total_questions=len(questions)
        current_category=category
        return jsonify(
            {
                'questions': page_questions,
                'totalQuestions': total_questions,
                'currentCategory': current_category
            }
        )
    
    @app.route('/questions', methods=["POST"])
    def create_question_or_search_questions():
        """
        Shared endpoint (app route) for create_question or search_questions - see above
        """
        body = request.get_json()
        search_term = body.get("searchTerm", None)
        if search_term is None:
            # Create question
            new_question = body.get("question", None)
            new_answer = body.get("answer", None)
            new_difficulty = body.get("difficulty", None)
            new_category = body.get("category", None)
            if new_question is None or new_answer is None or new_difficulty is None or new_category is None:
                abort(422)
            else:
                return create_question(new_question, new_answer, new_difficulty, new_category)
        else:
            # Search questions
            category = body.get("category", None)
            return search_questions(search_term, category)

    @app.route('/categories/<category_id>/questions')
    def retrieve_category_questions(category_id):
        """
        Endpoint to get questions based on category.
        Fetches questions for a cateogry specified by id request argument
        Request Arguments: id - integer
        Returns: An object with questions for the specified category, total questions, and current category string

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

    @app.route('/quizzes', methods=["POST"])
    def retrieve_next_question():
        """
        Endpoint to get questions to play the quiz.
        This endpoint takes category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
        Sends a post request in order to get the next question
        Returns: a single new question object

        POST '/quizzes'
        request body:
        {
            'previous_questions': [1, 4, 20, 15],
            'quiz_category': {
                'type': category_name, 
                'id': category_id
            }
        }
        reply:
        {
            'question': {
                'id': 1,
                'question': 'This is a question',
                'answer': 'This is an answer',
                'difficulty': 5,
                'category': 4
            }
        }
        """
        body = request.get_json()
        previous_questions = body.get("previous_questions", None)
        quiz_category = body.get("quiz_category", None)
        if quiz_category is None:
            abort(422)
        else:
            try:
                category_id = quiz_category['id']
                if category_id == 0: # ALL
                    question = Question.query.filter(Question.id.not_in(previous_questions)).first()
                else:
                    question = Question.query.filter(Question.category==str(category_id)).filter(Question.id.not_in(previous_questions)).first()
                return jsonify(
                    {
                        'question': question.format()
                    }
                )
            except:
                abort(422)

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
