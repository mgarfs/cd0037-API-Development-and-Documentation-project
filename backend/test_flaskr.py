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
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres',os.environ.get('POSTGRES_PWD'),'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after each test"""
        pass

    def test_retrieve_categories(self):
        """Test GET categories"""
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"])
        self.assertGreaterEqual(len(data["categories"]), 2) # expect more than one category

    def test_retrieve_questions(self):
        """Test GET questions, with optional page parameter"""
        # No page parameter
        res = self.client().get("/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertLessEqual(len(data["questions"]), 10) # max 10 questions per page
        self.assertGreaterEqual(len(data["questions"]), 1) # at least one question (otherwise it would be an error)
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(data["categories"])
        self.assertGreaterEqual(len(data["categories"]), 2)
        self.assertTrue(data["currentCategory"])
        # Page 1 - should be same as above (defaulting to page=1)
        res = self.client().get("/questions?page=1")
        data1 = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data, data1) # expect same content (for page 1) as without specifying page parameter
        # Page 2
        res = self.client().get("/questions?page=2")
        data2 = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(data2, data1) # expect different content (for page 2) from page 1
        self.assertTrue(data2["questions"])
        self.assertLessEqual(len(data2["questions"]), 10) # max 10 questions per page
        self.assertGreaterEqual(len(data2["questions"]), 1) # at least one question (otherwise it would be an error)
        self.assertTrue(data2["totalQuestions"])
        self.assertTrue(data2["categories"])
        self.assertGreaterEqual(len(data2["categories"]), 2)
        self.assertTrue(data2["currentCategory"])
        # Page 999 (non-existent)
        res = self.client().get("/questions?page=999")
        self.assertEqual(res.status_code, 404) # expecting not to find any questions on this far out page

    def test_retrieve_category_questions(self):
        """Test GET category questions"""
        # Questions for Category 1
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(data["currentCategory"])
        # Category 999 (non-existent)
        res = self.client().get("/categories/999/questions")
        self.assertEqual(res.status_code, 404)

    def test_delete_question(self):
        """Test DELETE question"""
        # Delete an exising question
        res = self.client().delete("/questions/5")
        self.assertEqual(res.status_code, 200)
        # Deleting the same question again - should result in error (showing that the previous attempt succeeded)
        res = self.client().delete("/questions/5")
        self.assertEqual(res.status_code, 422)

    def test_create_question(self):
        """Test create question"""
        # Create a new question
        new_question = {"question": "Is this the new answer string?", "answer": "Yes", "difficulty": 1, "category": 3}
        res = self.client().post("/questions", json=new_question)
        self.assertEqual(res.status_code, 200)

    def test_search_questions(self):
        """Test searching questions"""
        # Search for some questions - knowing the result will be non-empty
        res = self.client().post("/questions", json={"searchTerm": "title"})
        self.assertEqual(res.status_code, 200)
        # Search for some questions - knowing the result will be empty
        res = self.client().post("/questions", json={"searchTerm": "non_existing_term"})
        self.assertEqual(res.status_code, 200)
        # Invalid request body
        res = self.client().post("/questions", json={"searchForThis": "title"})
        self.assertEqual(res.status_code, 422)

    def test_retrieve_next_question(self):
        """Test retrieving next question (in quizz)"""
        # Ask for next question in Entertainment category (5)
        next_question = { 'previous_questions': [2, 4], 'quiz_category': { 'type': 'Entertainment', 'id': 5 } }
        res = self.client().post("/quizzes", json=next_question)
        self.assertEqual(res.status_code, 200)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
