import os
from flask import Flask, json, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/')
  def index():
    return "hello"

  ITEMS_PER_PAGE = 10
  def paginate_items(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    items = [item.format() for item in selection]
    current_items = items[start:end]

    return current_items

  @app.route('/questions', methods=['GET'])
  def get_questions():
    try:
      questions = Question.query.order_by(Question.id).all()
      current_questions = paginate_items(request, questions)
      categories = Category.query.all()
      categories_formatted = {category.id: category.type for category in categories} #TODO clean: extract the formatting
      return jsonify({
        'success': True,
        'questions': current_questions[0:10],
        'total_questions': len(questions),
        'categories': categories_formatted,
        'current_category': categories_formatted[1]
        })
    except:
      abort(422)

  @app.route('/questions', methods=['POST'])
  def add_or_search_question():
    try:
      body = request.get_json()
      if 'searchTerm' in body:
        searchTerm = body.get('searchTerm')
        print("SEARCH:", searchTerm)
        questions = Question.query.filter(Question.question.ilike('%{}%'.format(searchTerm))).all()
        current_questions = paginate_items(request, questions)
        categories = Category.query.all()
        categories_formatted = {category.id: category.type for category in categories} #TODO clean: extract the formatting
        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(questions),
          'current_category': categories_formatted[1]
          })

      else:
        question = body.get('question')
        answer = body.get('answer')
        difficulty = body.get('difficulty')
        category = body.get('category')
        new_question = Question(question, answer, category, difficulty)
        new_question.insert()
        print("QUESTION ADD:", question)

      return jsonify({
        'success': True
        })
    except:
      abort(422)

  @app.route('/questions/<id>', methods=['DELETE'])
  def delete_question(id):
    try:
      question = Question.query.get(id)
      if question is None:
        abort(404)
      question.delete()
      return jsonify({
        'success': True
        })
    except:
      abort(422)

  @app.route('/categories', methods=['GET'])
  def get_categories():
    try:
      categories = Category.query.all()
      categories_formatted = {category.id: category.type for category in categories} #TODO clean: extract the formatting
      return jsonify({
        'success': True,
        'categories': categories_formatted
        })
    except:
      abort(422)

  @app.route('/categories/<id>/questions', methods=['GET'])
  def get_questions_by_category(id):
    try:
      category = Category.query.get(id)
      questions = Question.query.filter(Question.category==category.id).all()      
      current_questions = paginate_items(request, questions)
      return jsonify({
        'success': True,
        'questions': current_questions,
        'current_category': {category.id: category.type}
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

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    