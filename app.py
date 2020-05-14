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
        if request.args.get('page') is None:
            page = 1
        else:
            page = int(request.args.get('page'))
        
        movies = Movie.query.order_by(Movie.id).paginate(page, MOVIES_PER_PAGE).items
        
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        })
        
        
    @app.route('/movies/<int:movie_id>', methods=['GET'])
    def get_single_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        
        if movie is None:
            abort(404)
        
        return jsonify({
            'success': True,
            'movie': movie.format()
        })
        
        
    @app.route('/movies', methods=['POST'])
    def post_movie():
        try:
            body = request.get_json()
            
            if body is None:
                abort(400)
                
            title = body.get('title', None)
            release_date = body.get('release_date', None)
            
            if title is None or release_date is None:
                abort(400)
                
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
            
            return jsonify({
                'success': True,
                'created': movie.id
            })
            
        except:
            abort(422)
        
    #TODO : Allow to add or remove new actors from movie
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def update_movie(movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
                
            if movie is None:
                abort(404)
            
            body = request.get_json()
            
            if body is None:
                abort(400)
                
            movie.title = body.get('title', movie.title)
            movie.release_date = body.get('release_date', movie.release_date)
                
            movie.update()
            
            return jsonify({
                'success': True,
                'updated': movie.id
            })
            
        except:
            abort(422)
    

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            
        if movie is None:
            abort(404)
                
        movie.delete()
            
        total_movies = Movie.query.order_by(Movie.id).count()
            
        return jsonify({
           'success': True,
           'total_movies': total_movies
        })


    '''
    Actors routes
    '''
    @app.route('/actors', methods=['GET'])
    def get_all_actors():
        if request.args.get('page') is None:
            page = 1
        else:
            page = int(request.args.get('page'))
        
        actors = Actor.query.order_by(Actor.id).paginate(page, ACTORS_PER_PAGE).items
        
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        })
    
    
    @app.route('/actors/<int:actor_id>', methods=['GET'])
    def get_single_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        
        if actor is None:
            abort(404)
        
        return jsonify({
            'success': True,
            'actor': actor.format()
        })
    

    @app.route('/actors', methods=['POST'])
    def post_actor():
        try:
            body = request.get_json()
            
            if body is None:
                abort(400)
                
            name = body.get('name', None)
            age = body.get('age', None)
            gender = body.get('gender', None)
            
            if name is None or age is None or gender is None:
                abort(400)
                
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()
            
            return jsonify({
                'success': True,
                'created': actor.id
            })
            
        except:
            abort(422)
            
            
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def update_actor(actor_id):
        try:
            # TODO : Check the value of 'gender'
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
                
            if actor is None:
                abort(404)
            
            body = request.get_json()
            
            if body is None:
                abort(400)
                
            actor.name = body.get('name', actor.name)
            actor.age = body.get('age', actor.age)
            actor.gender = body.get('gender', actor.gender)
                
            actor.update()
            
            return jsonify({
                'success': True,
                'updated': actor.id
            })
            
        except:
            abort(422)
    
            
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            
        if actor is None:
            abort(404)
                
        actor.delete()
            
        total_actors = Actor.query.order_by(Actor.id).count()
            
        return jsonify({
           'success': True,
           'total_actors': total_actors
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
