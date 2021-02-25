# Casting Agency

## Full Stack Nano - Capstone Project

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

There are different user roles (and related permissions), which are:

- Casting Assistant
    - Can view actors and movies
- Casting Director
   - All permissions a Casting Assistant has and…
   - Add or delete an actor from the database
   - Modify actors or movies

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

In the warranty-tracker directory, run the following to install all necessary dependencies:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server

To run the server, execute:
```
python3 app.py
```
We can now also open the application via Heroku using the URL:
https://capstone-saraalasfour.herokuapp.com/

The live application can only be used to generate tokens via Auth0, the endpoints have to be tested using curl or Postman 
using the token since I did not build a frontend for the application.

## API ARCHITECTURE AND TESTING
### Endpoint Library

@app.errorhandler decorators were used to format error responses as JSON objects. Custom @requires_auth decorator were used for Authorization based
on roles of the user. Two roles are assigned to this API: 'Casting Assistant' and 'Casting Director'.

A token needs to be passed to each endpoint. 
The following only works for /products endpoints:

#### GET '/actors'
Returns a list of actors in the database.
Sample response output:
```
{
    "actors": [
        {
            "age": "45",
            "gender": "male",
            "id": 1,
            "name": "Leonardo DiCaprio"
        },
        {
            "age": "42",
            "gender": "male",
            "id": 2,
            "name": "Jensen Ackles"
        },
        {
            "age": "70",
            "gender": "female",
            "id": 3,
            "name": "Meryl Streep"
        },
        {
            "age": "37",
            "gender": "female",
            "id": 4,
            "name": "Anne Hathaway"
        }
    ],
    "success": true
}
```
#### GET '/movies'
Returns a list of movies in the database.
Sample response output:
```
{
    "movies": [
        {
            "id": 1,
            "release": "December 19, 1997",
            "title": "Titatic"
        },
        {
            "id": 3,
            "release": "January 16, 2009",
            "title": "My Bloody Valentine"
        },
        {
            "id": 4,
            "release": "May 23rd, 1980",
            "title": "The Shining"
        }
    ],
    "success": true
}
```
#### POST '/create_actor'
Posts a new actor to the database, including the name, age, gender, and actor ID
Sample response output:
```
{
    "actor": {
        "age": "36",
        "gender": "male",
        "id": 6,
        "name": "Henry Cavill"
    },
    "success": true
}
```
#### POST '/create_movie'
Posts a new movie to the database, including the title, release, and movie ID
Sample response output:
```
{
    "movie": {
        "id": 5,
        "release": "November 3, 2017",
        "title": "Thor: Ragnarok"
    },
    "success": true
}
```
#### PATCH '/actors/int:id'
Patches an existing actor in the database.
```
{
    "actor": {
        "age": "36",
        "gender": "male",
        "id": 6,
        "name": "Henry Cavill"
    },
    "success": true
}
```
#### PATCH '/movies/int:id'
Patches an existing actor in the database.
```
{
    "movie": {
        "id": 5,
        "release": "November 3, 2017",
        "title": "Thor: Ragnarok"
    },
    "success": true
}
```
#### DELETE '/actors/int:actor_id'
Returns: ID for the deleted actor and status code of the request.```
```
{
	'deleted': 5,
	'success': true
}
```
#### DELETE '/movies/int:movie_id'
Returns: ID for the deleted actor and status code of the request.```
```
{
	'deleted': 5,
	'success': true
}
```
## Testing
There are 19 unittests in test_app.py. To run this file use:
```
dropdb agency_test
createdb agency_test
python3 test.py
```
The tests include one test for expected success and error behavior for each endpoint, and tests demonstrating role-based access control, 
where all endpoints are tested with and without the correct authorization.

## THIRD-PARTY AUTHENTICATION
#### auth.py
Auth0 is set up and running. The following configurations are in a .env file which is exported by the app:
- The Auth0 Domain Name
- The JWT code signing secret
- The Auth0 Client ID
The JWT token contains the permissions for the roles.

## DEPLOYMENT
The app is hosted live on heroku at the URL: 
 https://capstone-saraalasfour.herokuapp.com/
 
However, there is no frontend for this app yet, and it can only be presently used to authenticate using Auth0 by entering
credentials and retrieving a fresh token to use with curl or postman.
