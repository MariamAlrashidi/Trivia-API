import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category

class TriviaTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres','3224842','localhost:5432', self.database_name)
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
 
    def test_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        categories = Category.query.all()
        self.assertEqual(len(data['categories']), len(categories))

    def test_categories_unsuccessful(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        questions = Question.query.all()
        self.assertEqual(data['total_questions'], len(questions))

    def test_get_questions_unsuccessful(self):
        res = self.client().get('/questions/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Item not found.')


    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        questions = Question.query.all()
        self.assertEqual(data['total_questions'], len(questions))


    def test_get_paginated_questions_unsuccessful(self):
        res = self.client().post('/questions?page=999')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal Server Error.')


    def test_search(self):
        res = self.client().post('/search',
                                 json={'searchTerm': 'Who are you'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])



    def test_search_unsuccessful(self):
        res = self.client().get('/questions/search',
                                 json={'searchTerm': 'how are you'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Item not found.')

    def test_post_create_new_question(self):
        new_question_data = {
            'question': "what do you love",
            'answer': "I love programming",
            'category': 3,
            'difficulty': 2
        } 
        res = self.client().post('/questions', data=json.dumps(new_question_data), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_post_create_new_question_unsuccessful(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal Server Error.')


    # def test_delete_questions_successful(self):
    #     res = self.client().delete('/questions/34')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'],True)
    #     self.assertEqual(data['deleted'],34)
    #     self.assertEqual(data['total_questions'],38)


    # def test_delete_unsuccessful(self):
    #     res=self.client().post('/questions/34')
    #     data=json.loads(res.data)
    #     self.assertEqual(res.status_code,405)
    #     self.assertEqual(data['success'],False)
    #     self.assertEqual(data['message'],'METHOD NOT ALLOWED')


    def test_play_quiz_game_sccussful(self):
        response = self.client().post('/quizzes',
                                      json={'previous_questions': [19, 20],
                                            'quiz_category': {'type': 'Art', 'id': '5'}})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 5)
        self.assertNotEqual(data['question']['id'], 19)
        self.assertNotEqual(data['question']['id'], 20)


    def test_play_quiz_game_unsccussful(self):
        response = self.client().post('/quizzes')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal Server Error.')
 


    def test_get_questions_by_category_successful(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['questions']), 0)


    def test_if_questions_by_category_unsuccessful(self):
        response = self.client().get('/categories/100/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal Server Error.')

    def test_delete_question(self):
        last_question = Question.query.order_by(Question.id.desc()).first()
        if last_question is None:
            res = self.client().delete(f'/questions/{last_question.id}')
            data = json.loads(res.data)
            question = Question.query.filter(Question.id == last_question.id).one_or_none()
            self.assertSuccess(data, res.status_code)
            self.assertEqual(data['deleted_id'], last_question.id)
            self.assertNotEmpty(len(data['questions']))
            self.assertNotEmpty(data['totalQuestions'])
            self.assertEqual(question, None)
        else:
            pass

    def test_delete_question_unsuccessful(self):
        res = self.client().delete('/questions/999')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request could not be processed.')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
