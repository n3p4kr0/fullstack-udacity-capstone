import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import date

from app import create_app
from models.models import setup_db, Movie, Actor


class MovieTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.getenv('DB_TEST_URI')
        setup_db(self.app, self.database_path)

        self.casting_assistant = os.getenv('TOKEN_CASTING_ASSISTANT')
        self.casting_director = os.getenv('TOKEN_CASTING_DIRECTOR')
        self.executive_producer = os.getenv('TOKEN_EXECUTIVE_PRODUCER')

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies_successful(self):
        res = self.client().get('/movies',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_assistant)
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 10)

    def test_get_single_movie_successful(self):
        res = self.client().get('/movies/6',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_director)
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual((data['movie']['id']), 6)

    def test_get_single_movie_error_404(self):
        res = self.client().get('/movies/61993',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_director)
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_post_new_movie_successful(self):
        info = {
            'title': 'Test Movie',
            'release_date': date.today()
        }

        res = self.client().post('/movies',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.executive_producer)
                                 },
                                 json=info)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_new_movie_unauthorized(self):
        info = {
            'title': 'Test Movie',
            'release_date': date.today()
        }

        res = self.client().post('/movies',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.casting_director)
                                 },
                                 json=info)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_patch_movie_successful(self):
        info = {
            'title': 'Edited title',
        }

        res = self.client().patch('/movies/16',
                                  headers={
                                      "Authorization": "Bearer {}".format(
                                          self.casting_director)
                                  },
                                  json=info)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movie_error_404(self):
        info = {
            'title': 'Edited title',
        }

        res = self.client().patch('/movies/121303O',
                                  headers={
                                      "Authorization": "Bearer {}".format(
                                          self.casting_director)
                                  },
                                  json=info)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_delete_movie_successful(self):
        res = self.client().delete('/movies/17',
                                   headers={
                                       "Authorization": "Bearer {}".format(
                                           self.executive_producer)
                                   })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie_unauthorized(self):
        res = self.client().delete('/movies/5',
                                   headers={
                                       "Authorization": "Bearer {}".format(
                                           self.casting_director)
                                   })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)


class ActorTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.getenv('DB_TEST_URI')

        self.casting_assistant = os.getenv('TOKEN_CASTING_ASSISTANT')
        self.casting_director = os.getenv('TOKEN_CASTING_DIRECTOR')
        self.executive_producer = os.getenv('TOKEN_EXECUTIVE_PRODUCER')

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

    # TESTS FOR ACTORS

    def test_get_actors_successful(self):
        res = self.client().get('/actors',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_director)
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 10)

    def test_get_single_actor_successful(self):
        res = self.client().get('/actors/14',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_director)
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual((data['actor']['id']), 14)

    def test_get_single_actor_error_404(self):
        res = self.client().get('/actor/15873',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_assistant)
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_post_new_actor_successful(self):
        info = {
            'name': 'Brad Pitt',
            'age': 50,
            'gender': 'male'
        }

        res = self.client().post('/actors',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.executive_producer)
                                 },
                                 json=info)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_new_actor_unauthorized(self):
        info = {
            'name': 'Brad Pitt',
            'age': 50,
            'gender': 'male'
        }

        res = self.client().post('/actors',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.casting_assistant)
                                 },
                                 json=info)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_patch_actor_successful(self):
        info = {
            'name': 'Brad Pitt',
            'gender': 'male'
        }

        res = self.client().patch('/actors/53',
                                  headers={
                                      "Authorization": "Bearer {}".format(
                                          self.executive_producer)
                                  },
                                  json=info)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor_successful(self):
        res = self.client().delete('/actors/15',
                                   headers={
                                       "Authorization": "Bearer {}".format(
                                           self.executive_producer)
                                   })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor_unauthorized(self):
        res = self.client().delete('/actors/2',
                                   headers={
                                       "Authorization": "Bearer {}".format(
                                           self.casting_assistant)
                                   })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
