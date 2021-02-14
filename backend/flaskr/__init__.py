from __future__ import print_function  # In python 2.7

import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

import sys

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)

    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [q.format() for q in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={'/': {'origins': '*'}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type: application/json, Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')

        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''

    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()

        if len(categories) == 0:
            abort(404)

        categ_names = dict()
        for c in categories:
            categ_names[c.id] = c.type

        return jsonify({
            'success': True,
            'categories': categ_names
        })

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''

    @app.route('/questions', methods=['GET'])
    def get_question():
        selection = Question.query.all()
        current_questions = paginate_questions(request, selection)

        categories = Category.query.all()
        categ_names = dict()
        for c in categories:
            categ_names[c.id] = c.type

        if (len(current_questions) == 0):
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(current_questions),
            'categories': categ_names,
        })

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.filter(Question.id == id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question.id,
                'questions': current_questions,
                "total_questions": len(Question.query.all())
            })

        except:
            abort(422)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''

    @app.route('/questions', methods=['POST'])
    def post_question():
        body = request.json

        for parameter in ['question', 'answer', 'category', 'difficulty']:
            if parameter not in body:
                abort(422)

        question = body.get('question')
        answer = body.get('answer')
        category = body.get('category')
        diffculty = body.get('difficulty')

        try:
            new_question = Question(question, answer, category, diffculty)
            new_question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'created': new_question.id,
                'questions': current_questions,
                "total_questions": len(Question.query.all())
            })
        except:
            abort(422)

    '''
      @TODO:
      Create a POST endpoint to get questions based on a search term.
      It should return any questions for whom the search term
      is a substring of the question.

      TEST: Search by any phrase. The questions list will update to include
      only question that include that string within their question.
      Try using the word "title" to start.
      '''

    @app.route('/questions/search', methods=['POST'])
    def search_for_questions():
        body = request.json
        search_term = body.get('search_term')

        if search_term:
            questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

            formatted = [q.format() for q in questions]

            return jsonify({
                'success': True,
                'questions': formatted,
            })

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    @app.route('/categories/<int:id>/questions')
    def get_category_questions(id):
        questions = Question.query.filter(Question.category == id).all()
        formatted = [q.format() for q in questions]

        return jsonify({
            'success': True,
            'questions': formatted,
        })

    '''
      @TODO:
      Create a POST endpoint to get questions to play the quiz.
      This endpoint should take category and previous question parameters
      and return a random questions within the given category,
      if provided, and that is not one of the previous questions.

      TEST: In the "Play" tab, after a user selects "All" or a category,
      one question at a time is displayed, the user is allowed to answer
      and shown whether they were correct or not.
      '''

    @app.route('/quizzes', methods=['OPTIONS'])
    def start_game_preflight():
        print('PREFLIGHT---------------------', file=sys.stderr)

        return jsonify({
            'success': True,
        })

    @app.route('/quizzes', methods=['POST'])
    def start_game():
        print('--------------------', file=sys.stderr)
        body = request.json
        print(body, file=sys.stderr)

        category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')

        if category.id == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(
                category == category.id).all()

        in_previous = True
        new_question = False
        while(in_previous):
            new_question = questions[random.randrange(
                0, len(questions), 1)]
            if(new_question.id not in previous_questions):
                in_previous = False

        return jsonify({
            'success': True,
            'question': new_question.format()
        })

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request',
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found',
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable',
        }), 422

    return app


"""
curl http://127.0.0.1:5000/categories
curl http://127.0.0.1:5000/questions
curl http://127.0.0.1:5000/questions?page=2
curl -X DELETE http://127.0.0.1:5000/questions/22

curl -d 'question=1&answer=2&category=3&diffculty=4' -X POST http://127.0.0.1:5000/questions
curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d "{\"question\": \"1\",  \"answer\" : \"2\" ,  \"category\" : \"3\" ,  \"difficulty\" : \"2\" }"
curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d "{\"search_term\": \"ag\"}"

$env:FLASK_APP="flaskr"
$env:FLASK_ENV = "development"
flask run
"""
