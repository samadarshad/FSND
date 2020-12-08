import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'postgres', 'localhost:5432', self.database_name)
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
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
        delete_question = Question.query.filter(Question.question=='q1').all()
        [q.delete() for q in delete_question]
        delete_question = Question.query.filter(Question.question=='q1').all()
        self.assertFalse(delete_question)
        
        res = self.client().post('/questions', json={'question': 'q1', 'answer': 'a1', 'difficulty': 5, 'category': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        question = Question.query.filter(Question.question=='q1').first()
        self.assertTrue(question)
    # when wanting to test DELETE endpoint, do this: create a new question via backend, then delete using frontend endpoint - https://knowledge.udacity.com/questions/312483


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()