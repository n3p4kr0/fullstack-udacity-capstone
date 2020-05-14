import os
import sys
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from faker import Faker
import random

from models.models import setup_db, Actor, Movie

app = Flask(__name__)
database_path = os.getenv(sys.argv[1])
setup_db(app, database_path)


fak = Faker()

def populate_actors():
    i=1
    for i in range(101):
        Faker.seed(i)
        gender = ''
        if i%2 == 0:
            gender = 'male'
            name = fak.name_male()
        else:
            gender = 'female'
            name = fak.name_female()

        age = fak.random_int(18, 80)
        
        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()
        
def populate_movies():
    i=1
    for i in range(21):   
        Faker.seed(i+50)    
        title = fak.sentence(nb_words=fak.random_int(1,6))
        release_date = fak.date()
        
        movie = Movie(title=title, release_date=release_date)
        
        
        nb_actors_of_movie = fak.random_int(1, 5)
        j=0
        for j in range(nb_actors_of_movie):
            actor_id = fak.pyint(0,99)
            actor = Actor.query.filter(Actor.id == actor_id).one()
            movie.actors.append(actor)
        
        movie.insert()
            
    

if __name__ == '__main__':
    print('Populating database with fake Actors...')
    populate_actors()
    print('Populating database with fake Movies...')
    populate_movies()
    print('Done!')