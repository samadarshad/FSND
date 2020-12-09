from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from sqlalchemy.sql.expression import func
import error_handlers
from models import setup_db, Question, Category
from flasgger import Swagger

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.register_blueprint(error_handlers.blueprint)
    setup_db(app)
    CORS(app)
    swagger = Swagger(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
        return response

    @app.route('/')
    def index():
        return ("This is the backend page - "
                "start the frontend and go to localhost:3000")

    @app.route('/questions', methods=['GET'])
    def get_questions():
      """Returns a list of categories, current_category, question objects, success value, and total number of questions
      Results are paginated in groups of 10.
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: False
        default: 1
    definitions:
      Question:
        type: object
        properties:
          question:
            type: string
          answer:
            type: string
          category:
            type: integer
            $ref: '#/definitions/Category/properties/id'
          difficulty:
            type: integer
            description: 1 easiest, 5 hardest
      Category:
        type: object
        properties:
          id:
            type: integer
          type:
            type: string
    responses:
      200:
        description: A list of categories, current_category, question objects, success value, and total number of questions
        schema:
          properties:
            categories:
              type: object
              additionalProperties:
                $ref: '#/definitions/Category/properties/type'
            current_category:
              type: integer
            questions:
              type: array
              items:
                $ref: '#/definitions/Question'
            total_questions:
              type: integer
            success:
              type: boolean
      404:
        description: No questions found at given page
      500:
        description: Internal server error 
    """
      page = request.args.get('page', 1, type=int)
      questions = Question.query \
          .order_by(Question.id) \
          .paginate(page, QUESTIONS_PER_PAGE, error_out=False)
      current_questions = [q.format() for q in questions.items]
      if not current_questions:
          abort(404)
      try:
          categories = Category.query.all()
          categories_formatted = {category.id: category.type
                                  for category in categories}
          return jsonify({
              'success': True,
              'questions': current_questions,
              'total_questions': questions.total,
              'categories': categories_formatted,
              'current_category': None
          })
      except Exception:
          abort(500)

    @app.route('/questions', methods=['POST'])
    def add_or_search_question():
        """Add or Search a question.
    If 'searchTerm' is in request body, then it is a paginated search. Otherwise it is an add.
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: False
        default: 1
      - name: request
        in: body
        type: string
        required: False
        schema:
          type: object
          properties:
            searchTerm:
              type: string
            question:
              type: string
          example:
            searchTerm: title
            question: new question
            answer: new answer
            difficulty: 4
            category: 2
    responses:
      200:
        description: For search response - Returns a list of question objects that include the search term in its title, current_category, success value, and total number of questions found. For add response, just returns success value.
        schema:
          properties:            
            current_category:
              type: integer
            questions:
              type: array
              items:
                $ref: '#/definitions/Question'
            total_questions:
              type: integer
            success:
              type: boolean
      400:
        description: Bad request when adding a new question
      500:
        description: Internal server error
    """
        body = request.get_json()
        searchTerm = body.get('searchTerm', None)
        if searchTerm:
            try:
                page = request.args.get('page', 1, type=int)
                questions = Question.query \
                    .filter(Question.question.ilike('%{}%'.format(searchTerm))) \
                    .order_by(Question.id) \
                    .paginate(page, QUESTIONS_PER_PAGE, error_out=False)
                current_questions = [q.format() for q in questions.items]
                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': questions.total,
                    'current_category': None
                })
            except Exception:
                abort(500)

        else:
            question = body.get('question', None)
            answer = body.get('answer', None)
            difficulty = body.get('difficulty', None)
            category = body.get('category', None)
            if not question or not answer or not difficulty or not category:
                abort(400)
            try:
                new_question = Question(question, answer, category, difficulty)
                new_question.insert()
                return jsonify({
                    'success': True
                })
            except Exception:
                abort(500)

    @app.route('/questions/<id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.get(id)
        try:
            question.delete()
            return jsonify({
                'success': True
            })
        except Exception:
            abort(422)

    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()
            categories_formatted = {category.id: category.type
                                    for category in categories}
            return jsonify({
                'success': True,
                'categories': categories_formatted
            })
        except Exception:
            abort(500)

    @app.route('/categories/<id>/questions', methods=['GET'])
    def get_questions_by_category(id):
        category = Category.query.get(id)
        if not category:
            abort(404)
        try:
            page = request.args.get('page', 1, type=int)
            questions = Question.query \
                .filter(Question.category == category.id) \
                .order_by(Question.id) \
                .all()
            current_questions = [q.format() for q in questions]
            return jsonify({
                'success': True,
                'questions': current_questions,
                'current_category': category.id
            })
        except Exception:
            abort(500)

    @app.route('/quizzes', methods=['POST'])
    def post_question_to_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)
        if quiz_category:
            quiz_category = quiz_category['id']
        else:
            quiz_category = 0

        if (quiz_category == 0):
            query = Question.query
        else:
            query = Question.query.filter(Question.category == quiz_category)
        question = query.filter(~Question.id.in_(previous_questions)) \
            .order_by(func.random()).first()
        if question is None:
            abort(404)
        return jsonify({
            'success': True,
            'question': question.format()
        })

    return app
