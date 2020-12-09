from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from sqlalchemy.sql.expression import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

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

    ITEMS_PER_PAGE = 10

    def paginate_items(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE

        items = [item.format() for item in selection]
        current_items = items[start:end]

        return current_items

    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_items(request, questions)
        if not current_questions:
            abort(404)
        try:
            categories = Category.query.all()
            categories_formatted = {category.id: category.type
                                    for category in categories}
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions),
                'categories': categories_formatted,
                'current_category': None
            })
        except Exception:
            abort(500)

    @app.route('/questions', methods=['POST'])
    def add_or_search_question():
        body = request.get_json()
        searchTerm = body.get('searchTerm', None)
        if searchTerm:
            try:
                questions = Question.query \
                  .filter(Question.question.ilike('%{}%'.format(searchTerm))) \
                  .order_by(Question.id).all()
                current_questions = paginate_items(request, questions)
                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(questions),
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
            questions = Question.query \
              .filter(Question.category == category.id) \
              .order_by(Question.id).all()
            current_questions = paginate_items(request, questions)
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

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessible_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessible entity"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500

    return app
