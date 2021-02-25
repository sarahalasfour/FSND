import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
        actors = Actor.query.all()

        if len(actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        }), 200

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        movies = Movie.query.all()

        if len(movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(jwt, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'deleted': actor_id
            })

        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(jwt, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'deleted': movie_id
            })

        except:
            abort(422)

    @app.route('/create_actor', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(jwt):
        body = request.get_json()

        # actor = Actor()
        # actor.name = body['name']
        # actor.age = body['age']
        # actor.gender = body['gender']

        # new_name = body.get('name', None)
        # new_age = body.get('age', None)
        # new_gender = body.get('gender', None)

        try:
            actor = Actor(name=body['name'], age=body['age'], gender=body['gender'])
            actor.insert()

            return jsonify({
                'success': True,
                'actor': [actor.format() for actor in actor]
            })

        except:
            abort(422)

    @app.route('/create_movie', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(jwt):
        body = request.get_json()

        # movie = Movie()
        # movie.title = body['title']
        # movie.release = body['release']

        # new_title = body.get('title', None)
        # new_release = body.get('release', None)

        try:
            movie = Movie(title=body['title'], release=body['release'])
            # movie = Movie(title=new_title, release=new_release)
            movie.insert()

            return jsonify({
                'success': True,
                'movie': [movie.format() for movie in movie]
            })

        except:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(jwt, id):
        body = request.get_json()
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if actor is None:
            abort(404)

        try:
            get_name = body.get('name', None)
            get_age = body.get('age', None)
            get_gender = body.get('gender', None)

            if get_name:
                actor.name = get_name

            if get_age:
                actor.age = get_age

            if get_gender:
                actor.gender = get_gender

            actor.update()

            return jsonify({
                'success': True,
                'actors': [actor.format() for actor in actor]
            }), 200

        except:
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(jwt, id):
        body = request.get_json()
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if movie is None:
            abort(404)

        try:
            get_title = body.get('title', None)
            get_release = body.get('release', None)

            if get_title:
                movie.title = get_title

            if get_release:
                movie.release = get_release

            movie.update()

            return jsonify({
                'success': True,
                'movies': [movie.format() for movie in movie]
            }), 200

        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internet server error"
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response


    # @app.route('/')
    # def get_greeting():
    #     excited = os.environ['EXCITED']
    #     greeting = "Hello"
    #     if excited == 'true': greeting = greeting + "!!!!!"
    #     return greeting
    #
    # @app.route('/coolkids')
    # def be_cool():
    #     return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
