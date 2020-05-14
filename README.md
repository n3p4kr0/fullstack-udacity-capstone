# Full Stack Casting Agency API Backend

## Motivation

This project is the final project ("capstone") of Udacity's Fullstack Developer Nanodegree program.

It is a basic API backend of a casting agency management system.

Users can create Movies and Actors in the database, and link them (if an Actor is playing in a Movie).

Three roles (RBAC) are defined as is:

* Casting Assistant

A Casting Assistant is allowed to GET any single Movie or Actor, and to GET the lists of Movies and Actors.

* Casting Director

A Casting Director can do everything a Casting Assistant is allowed to. They can also remove (DELETE) any Movie or create (POST) one, and update (PATCH) any Movie or Actor.

* Executive Producer

An Executive Producer can do everything a Casting Director is allowed to. They can also remove (DELETE) any Actor or create (POST) one.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, you can populate the database with fixtures (generated from Faker). From the backend folder in terminal run:
```bash
python populator.py DB_URI
```

## Running the server

First ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app` directs flask to use the `app.py` file, which contains the main app methods.


## API Documentation
* GET "/movies?page=1"
    - Returns the list of all movies
    - Request Parameters: page
    - Response Body:
    
    `movies`: Dictionary of *Movie*:*actors[], id, release_date, title*
```json
{
  "success": true,
  "movies": [
    {
      "actors": [
        "Kimberly Wood",
        "John Butler",
        "James Chapman",
        "Kathryn Martin"
      ],
      "id": 3,
      "release_date": "Thu, 18 Nov 2004 00:00:00 GMT",
      "title": "They."
    },
    ...
  ]
}
```


* GET "/actors?page=1"
    - Returns the list of all Actors
    - Request Parameters: page
    - Response Body:
    
    `movies`: Dictionary of *Actor*:*id, name, gender, age, movies[]*
```json
{
  "success": true,
  "actors": [
    {
      "age": 23,
      "gender": "male",
      "id": 3,
      "movies": [
        "Lead represent view minute."
      ],
      "name": "Travis Brown"
    },
    ...
```


* POST "/actors"
    - Adds a new Actor to the database
    - Request Body:
    
    `age`: The Actors's age
    `name`: The Actors's name
    `gender`: The Actors's gender (`male` or `female`)
    - Response Body:
    
    `created`: Created Actor ID

    `total_actors`: Number of Actors after addition
```json
{
  "created": 102,
  "total_actors": 103,
  "success": true
}
```


* POST "/movies"
    - Adds a new Movie to the database
    - Request Body:
    
    `title`: The Movie's age
    `release_date`: The Actors's name
    - Response Body:
    
    `created`: Created Movie ID

    `total_movies`: Number of Actors after addition
```json
{
  "created": 13,
  "total_actors": 14,
  "success": true
}
```


* GET "/actors/<int:actor_id>"
    - Retrieves a single Actor from the database
    - Request Parameters: `actor_id`: ID of the Actor to delete
    - Response Body:

    `actor`: *Actor*:*id, name, gender, age, movies[]*
```json
{
  "actor": {
    "age": 47,
    "gender": "female",
    "id": 12,
    "movies": [
      "List model should.",
      "Its."
    ],
    "name": "Kristin Glass"
  },
  "success": true
}
```


* GET "/movies/<int:movie_id>"
    - Retrieves a single Movie from the database
    - Request Parameters: `movie_id`: ID of the Movie to delete
    - Response Body:

    `movie`: *Movie*:*id, title, release_date, actors[]*
```json
{
  "movie": {
    "actors": [
      "Kristin Pacheco"
    ],
    "id": 12,
    "release_date": "Mon, 04 Nov 1991 00:00:00 GMT",
    "title": "News special fly."
  },
  "success": true
}
```


* PATCH "/actors/<int:actor_id>"
    - Modifies an Actor in the database
    - Request Parameters: `actor_id`: ID of the Actor to update
    - Response Body:

    `updated`: Updated Actor's ID
```json
{
  "success": true,
  "updated": 20
}
```


* PATCH "/movies/<int:movie_id>"
    - Modifies a Movie in the database
    - Request Parameters: `movie_id`: ID of the Movie to update
    - Response Body:

    `updated`: Updated Movie's ID
```json
{
  "success": true,
  "updated": 20
}
```


* DELETE "/actors/<int:actor_id>"
    - Deletes an Actor in the database
    - Request Parameters: `actor_id`: ID of the Actor to delete
    - Response Body:

    `deleted`: Deleted Actor's ID
    `total_actors`: Number of Actors remaining after deletion
```json
{
  "success": true,
  "deleted": 20,
  "total_actors": 19
}
```



* DELETE "/movies/<int:movie_id>"
    - Deletes an Movie from the database
    - Request Parameters: `movie_id`: ID of the Movie to delete
    - Response Body:

    `deleted`: Deleted Movie's ID
    `total_movies`: Number of Movies remaining after deletion
```json
{
  "success": true,
  "deleted": 20,
  "total_movies": 19
}
```


## Testing
To run the tests, run
```
dropdb casting_agency_test
createdb casting_agency_test
python populator.py DB_TEST_URI
python tests.py
```