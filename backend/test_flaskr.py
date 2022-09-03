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
        self.database_path = "postgresql://{}:{}@{}/{}".format(
    "student", "student", "localhost:5432", self.database_name
)
        setup_db(self.app, self.database_path)

        self.new_question = {"question":"What year did Nigeria gain her Independence?", "answer":"1960", "category":1, "difficulty":3}
        self.new_quiz_question_request_body = {"previous_questions":[],"quiz_category": {"type":"history", "id": 4}}
        self.new_quiz_question_with_empty_question_request_body = {"previous_questions":[13,14,15],"quiz_category": {"type":"geography", "id": 3}}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
      res = self.client().get('/categories')
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(data['total_categories'])
      self.assertTrue(len(data['categories']))

    def test_get_paginated_questions(self):
      res = self.client().get('/questions')
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(len(data['questions']))
      self.assertTrue(data['total_questions'])
      self.assertTrue(data['categories'])

    def test_404_sent_requesting_beyond_valid_page(self):
      res = self.client().get('/questions?page=1000')
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 404)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
      res = self.client().delete('/questions/2')
      data = json.loads(res.data)
      question = Question.query.filter(Question.id == 2).one_or_none()

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
      res = self.client().delete('/questions/1000')
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 422)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_question(self):
      res = self.client().post('/questions', json=self.new_question)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
    
    def test_405_if_question_creation_not_allowed(self):
      res = self.client().post('/questions/45', json=self.new_question)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 405)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'method not allowed')

    def test_get_questions_search_with_results(self):
      res = self.client().post('/questions/search', json={"searchTerm": "Africa"})
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(data['total_questions'])
      self.assertEqual(len(data['questions']), 1)

    def test_get_questions_search_without_result(self):
      res = self.client().post('/questions/search', json={"searchTerm": 'impossible123'})
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertEqual(data['total_questions'], 0)
      self.assertEqual(len(data['questions']), 0)

    def test_get_category_questions(self):
      res = self.client().get('/categories/3/questions')
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertEqual(len(data['questions']), 3)
      self.assertEqual(data['total_questions'], 3)
      self.assertEqual(data['current_category'], 'Geography')

    def test_get_category_questions_that_does_not_exist(self):
      res = self.client().get('/categories/9/questions')
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 400)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'bad request')

    def test_get_quiz_question(self):
      res = self.client().post('/quizzes', json=self.new_quiz_question_request_body)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(data['question'])
      self.assertEqual(data['question']['category'], 4)

    def test_get_quiz_question_with_empty_question_response(self):
      res = self.client().post('/quizzes', json=self.new_quiz_question_with_empty_question_request_body)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertEqual(data['question'], None)





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()