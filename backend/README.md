# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## API Documentation

GET '/questions'

- Returns questions, where each question has id, question, answer, category, difficulty
- pagination is allowed by including a "page" query parameter with an integer value, the value should return 10 questions or less
- Request: '/questions?page=1' page is optional
- Response:
  {
  'success': True,
  'questions': current_questions,
  'total_questions': len(current_questions),
  'categories': categ_names,
  }

GET '/categories'

- Returns all the categories
- Request: '/categories'
- Response
  {
  "categories": {
  "1": "history",
  "2": "science",
  "3" : "Geography",
  "4" : "History",
  "5" : "Entertainment",
  "6" : "Sports"
  },
  "success": true
  }

DELETE '/questions/question_id'

- Deletes a question given an id in the request body
- Request: '/questions/question_id'
- Response:
  {
  'success': True,
  'deleted': question_id,
  'questions': current_questions,
  "total_questions": number_of_questions
  }

POST '/questions'

- Adds a new question given its parameters (id, question, answer, category, difficulty)
- Request: '/questions'
  {
  "answer": "blue",
  "category": "2",
  "difficulty": 1,
  "id": 10,
  "question": "What is the colour of sky"
  }

- Response:
  {
  'success': True,
  'created': new_question_id,
  'questions': current_questions,
  "total_questions": number_of_questions
  }

POST '/questions/search'

- Searches for a question given a search_term
- Request: '/questions/search'
  {
  'searchTerm' : 'what'
  }
- Response:
  {
  'success': True,
  'questions': questions,
  }

GET '/categories/category_id/questions'

- Fetches questions given a specific category
- Request Arguments: '/categories/category_id/questions'
- Response:
  {
  'success': True,
  'questions': questions,
  }

POST '/quizzes'

- Starts the game by fetching questions given a category
- Request Arguments: '/quizzes'
  {
  'quiz_category' : quiz_category
  'previous_questions' : previous_questions_ids
  }
- Response:
  {
  'success': True,
  'question': question
  }
