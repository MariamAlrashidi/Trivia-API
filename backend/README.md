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

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

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

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 
Intro The Trivia API is an API developed to be incorporated into a frontend trivia game for Udacity students. The API has connects to a database (name trivia) with a number of trivia questions that include question answers, difficulty levels, and a number of categories.

Errors 400 404 422 500

Note: all error handlers return a JSON object with the request status and error message.

400

400 error handler is returned when the request cannot be completed. This may be due to being malformed or missing arguments.
{
	"error": 400,
	"message": "Bad request.",
	"success": false
}
404

404 error handler occurs when a request resource cannot be found in the database, i.e. a question with a nonexistent ID is requested.
{
	"error": 404,
	"message": "Item not found.",
	"success": false
}
422

422 error handler is returned when the request contains invalid arguments, i.e. a difficulty level that does not exist.
{
	"error": 422,
	"message": "Request could not be processed.",
	"success": false
}
500

500 error handler is returned on server errors, i.e. a request is sent when the server is unavailable or not running.
{
	"error": 500,
	"message": "Internal Server Error.",
	"success": false
}
Endpoints GET '/categories' GET '/questions' POST '/questions' POST '/search' POST 'quizzes' DELETE '/questions/<int:quest_id>'

GET '/categories'

Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
Request Arguments: None
Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{
	"categories": {
		"1": "Science",
		"2": "Art",
		"3": "Geography",
		"4": "History",
		"5": "Entertainment",
		"6": "Sports"
	},
	"success": true
}
GET '/questions', '/questions/int:page'

Fetches a dictionary of all questions in the database with keys and values for the question answer, question difficulty, question ID, and question category. Also includes the categories dictionary for reference, as well as a 'next url' link for the next url in the pagination order.
Request Arguments: Page number (Optional). Pages include ten questions per page by default. Jump to the next page using an integer argument for each page number.
Returns: A questions object with the question, answer, question ID, difficult, and category.
{
	"answer": "Tom Cruise",
	"category": 5,
	"difficulty": 4,
	"id": 4,
	"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
}
POST '/questions

Posts a new question to the database, including the question, the question answer, difficulty level, and category. ID is automatically assigned upon assertion.
Request arguments: Question, answer, category (integer or string), and difficulty level (integer, levels 1-5). All arguments are required and must be passed in the body as a JSON object.
{
	"answer": "Muhammad Ali",
	"category": 4,
	"difficulty": 1,
	"question": "What boxer's original name is Cassius Clay?'"
}
Returns: A dictionary object that includes the question, answer, category, difficulty, and newly assigned question ID, as well as the status of the request.
{
	"question": {
		"answer": "Maya Angelou",
		"category": 4,
		"difficulty": 2,
		"id": 34,
		"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
	},
	"success": true
}
POST '/search'

Fetches any questions that include the search term in the body of the question.
Request arguments: Search tearm (string), which must be passed in the body as a JSON string. Required.
{
	"searchTerm": "boxer"
}
Returns: A dicitionary object that includes all relevant questions, including each question, question ID, question anwer, category, and difficulty.
{
	"questions": [
		{
			"answer": "Apollo 13",
			"category": 5,
			"difficulty": 4,
			"id": 2,
			"question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
		}
	],
	"success": true,
	"totalQuestions": 1
}
POST 'quizzes'

Fetches a random question from within a category, without repeating previously passed questions.
Request arguments: Category (optional). Category can be passed as either an integer or a string and must be passed as a JSON string.
{
	"category": 3
}
Returns: A JSON object including the category, previous question list, and a question dictionary object.
{
    "category": 3,
    "previous_questions": [],
    "question": {
        "answer": "The Palace of Versailles",
        "category": 3,
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    "success": true
}
DELETE '/questions/int:quest_id'

Deletes a question in the database via the DELETE method and using the question id.
Request argument: Question id, included as a parameter following a forward slash (/).
Returns: ID for the deleted question and status code of the request.
{
	'id': 5,
	'success': true
}
Testing
To run the tests, run

dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py