import os
from flask import Flask, request, abort, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection, page):
  if not page:
    page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  questions_displayed = questions[start:end]
  return questions_displayed




def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
      response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type,Authorization,true'
      )
      response.headers.add(
        'Access-Control-Allow-Methods',
        'GET,PATCH,POST,DELETE,OPTIONS'
      )
      return response

# ----------------------------------------------------------------------
# Endpoints
# ----------------------------------------------------------------------

  # Endpoint to handle GET requests for all available categories here.
  @app.route('/categories', methods=['GET'])
  def get_categories():
      categories = Category.query.all()
      if not categories:
        abort(404)

      return jsonify({
        'success': True,
        'categories': {category.id:category.type for category in categories},
        'total_categories': len(Category.query.all()),
      }), 200

  # Endpoint to handle GET requests for questions, paginate by QUESTIONS_PER_PAGE, show all questions.
  @app.route('/questions', methods=['GET'])
  def get_questions():
    # Get categories for JSON return for frontend
    categories = Category.query.all()
    # Get all questions here
    questions = Question.query.order_by(Question.id).all()
    questions_displayed =paginate_questions(request, questions, 1)
    if not questions_displayed:
      abort(404)

    return jsonify({
      'questions': questions_displayed,
      'categories': {category.id:category.type for category in categories},
      'success': True,
      'total_questions': len(Question.query.all()),
      }), 200

  # Endpoint to handle GET request for questions, paginate by QUESTIONS_PER_PAGE and filter by category id
  # Uses page_questions for the pagination.
  @app.route('/categories/<category>/questions', methods=['GET'])
  def get_questions_by_category(category, page=False):
    category_data = False

    # Checks for valid category id
    if category.isnumeric():
      category_data = Category.query.get(category)
      category_id = category

    # Checks for category type and converts to id if found that
    if not category_data:
      category_data = Category.query.filter_by(type=category).first()
      category_id = category_data.id

    # If category is not found, return error message
    if not category_data:
      abort(400)

    questions = Question.query.filter_by(category=category_id).all()
    questions_displayed = paginate_questions(request, questions, page=page)

    # If page number does not exist, returns 404
    if not questions_displayed:
      abort(404)

    return jsonify({
      'questions': questions_displayed,
      'success': True,
      'total_questions': len(questions),
      'next_url': url_for('get_questions_by_category', category=category, page=page+1)
      }), 200

  # Endpoint to handle DELETE request using question ID
  @app.route('/questions/<int:quest_id>', methods=['DELETE'])
  def delete_question(quest_id, page=False):
      try:
          question = Question.query.filter(
            Question.id == quest_id
            ).one_or_none()

          if question is None:
              abort(404)

          question.delete()

          questions = Question.query.order_by(Question.id).all()
          questions_displayed = paginate_questions(request, questions, page=page)

          return jsonify({
              "success": True,
              "deleted_id": quest_id,
              "questions": questions_displayed,
              "totalQuestions": len(Question.query.all()),
          })

      except:
          abort(422)

  @app.route('/questions', methods=['POST'])
  def add_question():
      body = request.get_json()

      new_question = body.get('question')
      new_answer = body.get('answer')
      new_difficulty = body.get('difficulty')
      new_category = body.get('category')
              # create and insert new question
      question = Question(question=new_question, answer=new_answer,
                          difficulty=new_difficulty, category=new_category)
      question.insert()

      # get all questions
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection, 1)

      return jsonify({
          'success': True,
          'current_questions': current_questions,
          'total_questions': len(Question.query.all())
      })
              
  # Endpoint to handle search request
  @app.route('/search', methods=['POST'])
  def find_questions():
        from_body = request.get_json()

        search = from_body.get('searchTerm')
        submitSearch = Question.query.order_by(Question.id).filter(
            Question.question.ilike('%{}%'.format(search)))
        add_question = paginate_questions(request, submitSearch, 1)

        return jsonify({
            "success": True,
            "questions": add_question,
            "totalQuestions": len(add_question),
        })
  # Endpoint to play quiz that filter by category and previous questions that have been answer. 
  @app.route('/quizzes', methods=['POST'])
  def get_quiz_quetion():
        body = request.get_json()
        previous_questions_ids = body.get('previous_questions')
        category_id = body.get('quiz_category')['id']

        questions = []
        formatted_next_question = None

        if category_id == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter(
              Question.category == category_id,
              Question.id.notin_(previous_questions_ids)
              ).all()

        if len(questions) == 0:
            formatted_next_question = None
        if len(questions) > 0:
            next_question = random.choice(questions)
            formatted_next_question = next_question.format()

        return jsonify({
            "success": True,
            "question": formatted_next_question
        })


# ----------------------------------------------------------------------
# Error handlers
# ----------------------------------------------------------------------

  #Error handler for malformed requests.
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "Bad request."
      }), 400

  #Error handler for objects that cannot be found in  db.
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Item not found."
      }), 404
      
  #Error handler for requests 
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "Request could not be processed."
      }), 422

  #Error handler for when server fails. 
  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "Internal Server Error."
      }), 500

  #Error handler for when Mehod Not Allowed. 
  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "Method Not Allowed"
      }), 405


# ----------------------------------------------------------------------
# Runs app
# ----------------------------------------------------------------------

  return app