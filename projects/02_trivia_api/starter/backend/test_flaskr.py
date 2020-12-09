import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'trivia_test')
DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = DB_PATH
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        expected_questions = Question.query.order_by(Question.id).all()
        expected_questions_formatted = [q.format() for q in expected_questions]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['questions'], expected_questions_formatted[0:10])
        self.assertEqual(data['total_questions'], len(expected_questions_formatted))

    def test_404_when_get_questions_beyond_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource not found")

    def test_add_question(self):
        # setup: clear all questions 'q1'
        delete_question = Question.query.filter(Question.question=='q1').all()
        [q.delete() for q in delete_question]
        delete_question = Question.query.filter(Question.question=='q1').all()
        self.assertFalse(delete_question)

        # test
        res = self.client().post('/questions', json={'question': 'q1', 'answer': 'a1', 'difficulty': 5, 'category': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        question = Question.query.filter(Question.question=='q1').first()
        self.assertTrue(question)

        # teardown: clear all questions 'q1'
        delete_question = Question.query.filter(Question.question=='q1').all()
        [q.delete() for q in delete_question]
        delete_question = Question.query.filter(Question.question=='q1').all()
        self.assertFalse(delete_question)

    def test_400_if_add_empty_question(self):
        res = self.client().post('/questions', json={'question': None, 'answer': 'a1', 'difficulty': 5, 'category': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad request")

    def test_search_question(self):
        res = self.client().post('/questions', json={'searchTerm': 'title'}) #this is question id 5 and 6 in the test database
        data = json.loads(res.data)
        expected_questions = [Question.query.get(5).format(), Question.query.get(6).format()]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['questions'], expected_questions)
        self.assertEqual(data['total_questions'], 2)

    def test_delete_question(self):
        # setup: clear all questions 'q1'
        delete_question = Question.query.filter(Question.question=='q1').all()
        [q.delete() for q in delete_question]

        # setup: add question 'q1'
        add_question = Question('q1', 'a1', 5, 1)
        add_question.insert()
        question = Question.query.filter(Question.question=='q1').all()
        self.assertTrue(question)

        res = self.client().delete('/questions/{}'.format(add_question.id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        question = Question.query.filter(Question.question=='q1').first()
        self.assertFalse(question)

    def test_422_if_delete_nonexisting_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessible entity")

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        expected_categories = Category.query.all()
        expected_categories_formatted = {str(category.id): category.type for category in expected_categories}
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['categories'], expected_categories_formatted)

    def test_405_if_post_to_categories(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method not allowed")

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions') #questions in category 1 are id:20, 21 and 22
        data = json.loads(res.data)
        
        expected_questions = [Question.query.get(20).format(), Question.query.get(21).format(), Question.query.get(22).format()]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['current_category'], 1)
        self.assertEqual(data['questions'], expected_questions)

    def test_404_if_get_nonexisting_category(self):
        res = self.client().get('/categories/100/questions') 
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource not found")

    def test_post_random_question_to_quiz(self):
        res = self.client().post('/quizzes', json={'quiz_category': {'id': 0}, 'previous_questions': []}) 
        data = json.loads(res.data)
        minimumId = Question.query.order_by(Question.id).first().id
        maximumId = Question.query.order_by(Question.id.desc()).first().id

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertTrue(minimumId <= data['question']['id'] <= maximumId)

    def test_404_if_quiz_category_nonexist(self):
        res = self.client().post('/quizzes', json={'quiz_category': {'id': 1000}, 'previous_questions': []}) 
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource not found")

    def test_post_non_previous_quiz_question(self):
        res = self.client().post('/quizzes', json={'quiz_category': {'id': 6}, 'previous_questions': []}) #category 6 only has questions of id 10 and 11
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn(data['question']['id'], [10, 11])

        res = self.client().post('/quizzes', json={'quiz_category': {'id': 6}, 'previous_questions': [10]}) 
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn(data['question']['id'], [11])

    def test_404_if_no_quiz_question_remains(self):
        res = self.client().post('/quizzes', json={'quiz_category': {'id': 6}, 'previous_questions': [10, 11]}) 
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource not found")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()