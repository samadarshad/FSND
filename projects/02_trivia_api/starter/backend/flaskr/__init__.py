from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from sqlalchemy.sql.expression import func
import error_handlers
from models import setup_db, Question, Category
from flasgger import Swagger, swag_from

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
    @swag_from('api_doc/questions_get.yml')
    def get_questions():        
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
    @swag_from('api_doc/questions_post.yml')
    def add_or_search_question():        
        body = request.get_json()
        searchTerm = body.get('searchTerm', None)
        if searchTerm:
            try:
                page = request.args.get('page', 1, type=int)
                questions = Question.query \
                    .filter(
                        Question.question.ilike('%{}%'.format(searchTerm))) \
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
    @swag_from('api_doc/questions_delete.yml')
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
    @swag_from('api_doc/categories_get.yml')
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
    @swag_from('api_doc/categories_id_questions_get.yml')
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
    @swag_from('api_doc/quizzes_post.yml')
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
