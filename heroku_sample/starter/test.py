import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

# from flaskr import create_app
from models import setup_db, Actor, Movie


class AgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = "postgres://{}@{}/{}".format('saraalasfour','localhost:5432', self.database_name)
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
    Write at least one test for each test for successful operation and for expected errors.
    """


    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_404_sent_requesting_not_exist_actor(self):
        res = self.client().get('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_404_sent_requesting_not_exist_movie(self):
        res = self.client().get('/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actor(self):
        actor = Actor(name="Anne Hathaway", age="37", gender="female")
        actor.insert()

        actor_id = actor.id

        res = self.client().delete(f'/actors/{actor_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor_id)
        self.assertEqual(data['message'], 'Question successfully deleted')

    def test_422_sent_deleting_not_exist_actor(self):
        res = self.client().delete('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_movie(self):
        movie = Movie(title="Invisible Man", release="March 20, 2020")
        movie.insert()

        movie_id = movie.id

        res = self.client().delete(f'/movies/{movie_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie_id)
        self.assertEqual(data['message'], 'movie successfully deleted')

    def test_422_sent_deleting_not_exist_movie(self):
        res = self.client().delete('/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_actor(self):
        actors_before_create = len(Actor.query.all())
        new_actor = {
            'name': 'New name',
            'age': 'New age ',
            'gender': 'New gender '
        }
        res = self.client().post('/create_actor', data=json.dumps(new_actor), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        actors_after_create = len(Actor.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue((actors_after_create - actors_before_create) == 1)

    def test_422_create_actor_with_empty_data(self):
        new_actor = {
            'name': 'New name',
            'age': 'New age',
            'gender': ''
        }
        res = self.client().post('/create_actor', data=json.dumps(new_actor), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_create_movie(self):
        movies_before_create = len(Movie.query.all())
        new_movie = {
            'title': 'New title',
            'release': 'New release'
        }
        res = self.client().post('/create_movie', data=json.dumps(new_movie), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        movies_after_create = len(Movie.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue((movies_after_create - movies_before_create) == 1)

    def test_422_create_movie_with_empty_data(self):
        new_movie = {
            'title': 'New title',
            'release': ''
        }
        res = self.client().post('/create_movie', data=json.dumps(new_movie), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_update_existing_actor(self):
        actor = Actor(name="Anne Hathaway", age="100", gender="female")
        actor.insert()
        actor_id = actor.id

        actor_data_patch = {
            'age': '37'
        }

        res = self.client().patch(
            f'/actors/{actor_id}',
            data=json.dumps(actor_data_patch),
            headers={'Content-Type': 'application/json'}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], actor.name)
        self.assertEqual(data['actor']['age'], actor_data_patch['age'])
        self.assertEqual(data['actor']['gender'], actor.gender)

        actor_updated = Actor.query.get(data['actor']['id'])
        self.assertEqual(actor_updated.id, actor.id)

    def test_update_not_exist_actor(self):
        actor_data_patch = {
            'age': '1'
        }

        res = self.client().patch('/actors/1000', data=json.dumps(actor_data_patch), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])

    def test_update_existing_movie(self):
        movie = Movie(title="Invisible Man", release="March 20, 1998")
        movie.insert()
        movie_id = movie.id

        movie_data_patch = {
            'release': 'March 20, 2020'
        }

        res = self.client().patch(
            f'/movies/{movie_id}',
            data=json.dumps(movie_data_patch),
            headers={'Content-Type': 'application/json'}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], movie.title)
        self.assertEqual(data['movie']['release'], movie_data_patch['release'])

        movie_updated = Movie.query.get(data['movie']['id'])
        self.assertEqual(movie_updated.id, movie.id)

    def test_update_not_exist_movie(self):
        movie_data_patch = {
            'title': 'Foo'
        }

        res = self.client().patch('/movies/1000', data=json.dumps(movie_data_patch), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()