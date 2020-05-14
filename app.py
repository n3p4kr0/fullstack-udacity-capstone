import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth


MOVIES_PER_PAGE = int(os.getenv('MOVIES_PER_PAGE'))
ACTORS_PER_PAGE = int(os.getenv('ACTORS_PER_PAGE'))


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    # Set up CORS
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

 
    @app.route('/', methods=['GET'])
    def home_route():
        return jsonify({
            'success': True,
            'message': 'Route Working'
        })
        
    '''
    Movies routes
    '''
    @app.route('/movies', methods=['GET'])
    def get_all_movies():
        page = int(request.args.get('page'))
        movies = Movie.query.order_by(Movie.id).paginate(page, MOVIES_PER_PAGE).items
        
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        })
        

    '''
    Actors routes
    '''
    @app.route('/actors', methods=['GET'])
    def get_all_actors():
        page = int(request.args.get('page'))
        actors = Actor.query.order_by(Actor.id).paginate(page, ACTORS_PER_PAGE).items
        
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        })
        

    # Error Handling
    '''
    Example error handling for unprocessable entity
    '''
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


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404


    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "message": error.error
        }), error.status_code

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
