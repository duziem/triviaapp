import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get("page", 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # CORS(app)
    CORS(app, resources={r"/foo": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
      try:
        categories = Category.query.all()
        formatted_categories = {}
        for category in categories:
          formatted_categories[category.id] = category.type
        return jsonify({
          'success': True,
          'categories': formatted_categories,
          'total_categories': len(formatted_categories)
        })
      except:
        print(sys.exc_info())
        abort(400)

    @app.route('/questions', methods=['GET'])
    def get_questions():
      selection = Question.query.order_by(Question.id).all()
      questions = paginate_questions(request, selection)
      if (len(questions) == 0):
        abort(404)
      
      categories = Category.query.all()
      formatted_categories = {}
      for category in categories:
        formatted_categories[category.id] = category.type

      return jsonify({
        'success': True,
        'questions': questions,
        'total_questions': len(Question.query.all()),
        'categories': formatted_categories
      })

    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
      try:
        body = request.get_json()
        question = Question.query.get(question_id)
        if question is None:
          abort(404)
        question.delete()
        return jsonify({
          'success': True,
        })
      except:
        abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
      body = request.get_json()
      new_question = body.get("question", None)
      new_answer = body.get("answer", None)
      new_category = body.get("category", None)
      new_difficulty = body.get("difficulty", None)
      try:
        question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
        question.insert()
        return jsonify({
          'success': True,
        })
      except:
        print(sys.exc_info())
        abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
      body = request.get_json()
      search = body.get("searchTerm", None)
      try:
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
        questions = paginate_questions(request, selection)
        return jsonify({
          'success': True,
          'questions': questions,
          'total_questions': len(selection.all())
        })
      except:
        abort(422)

    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def get_category_questions(category_id):
      try:
        category = Category.query.filter_by(id=category_id).one_or_none()
        selection = Question.query.order_by(Question.id).filter_by(category=category_id)
        questions = paginate_questions(request, selection)

        return jsonify({
          'success': True,
          'questions': questions,
          'total_questions': len(selection.all()),
          'current_category': category.type
        })
      except:
        print(sys.exc_info())
        abort(400)

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
      body = request.get_json()
      quiz_category = body.get("quiz_category", None)
      previous_questions = body.get("previous_questions")
      try:
        if quiz_category['id'] == 0:
          questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
        else:
          questions = Question.query.filter(Question.id.notin_(previous_questions), Question.category == quiz_category['id']).all()

        question = None
        if(questions):
          question = random.choice(questions).format()
        return jsonify({
          'success': True,
          'question': question
        })

      except:
        print(sys.exc_info())
        abort(422)

    @app.errorhandler(404)
    def not_found(error):
      return jsonify({"success": False, "error": 404, "message": "resource not found"}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({"success": False, "error": 405, "message": "method not allowed"}), 405

    return app

