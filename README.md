## Trivia App

The application can:

1. Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.


### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 405: Method not allowed

### Endpoints 
### GET '/categories'
- General:
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
- Sample: `curl http://127.0.0.1:5000/categories`

``` {
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true, 
  "total_categories": 6
}
```

### GET '/questions'
- General:
    - Fetches a list of questions and categories
    - Request Arguments: Page (to request page number starting from 1)
    - Returns: a list of question objects paginated in groups of 10, success value, total number of questions, and a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Sample: `curl http://127.0.0.1:5000/questions`

``` {
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```

#### POST /questions
- General:
    - Creates a new question.
    - Request Body: Question, Answer, Category and Difficulty. 
    - Returns: Success value. 
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What year did Nigeria gain her Independence?", "answer":"1960", "category":1, "difficulty":3}'`
```
{
  "success": true
}
```
#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. 
    - Request Parameter: question_id
    - Returns: Success value.
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/2`
```
{
  "success": true
}
```
#### POST /questions/search
- General:
    - fetches questions based on a search term
    - Request Body: searchTerm
    - Returns: list of questions paginated in groups of 10, success value and total number of questions
- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"Clay"}'`
```
{
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

#### GET /categories/<category_id>/questions
- General:
    - fetches questions based on the category chosen
    - Request Parameter: category_id
    - Returns: list of questions paginated in groups of 10, success value, current category and total number of questions
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`
```
 
{
  "current_category": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Yes he is", 
      "category": 1, 
      "difficulty": 1, 
      "id": 49, 
      "question": "Is ayo a boy?"
    }, 
    {
      "answer": "1960", 
      "category": 1, 
      "difficulty": 3, 
      "id": 50, 
      "question": "What year did Nigeria gain her Independence?"
    }, 
    {
      "answer": "1960", 
      "category": 1, 
      "difficulty": 3, 
      "id": 51, 
      "question": "What year did Nigeria gain her Independence?"
    }
  ], 
  "success": true, 
  "total_questions": 6
}
```

#### POST /quizzes
- General:
    - Fetches questions randomly and within the given category if provied without repeating a previous question to play the quiz
    - Request Body: quiz_category, previous_questions
    - Returns: A question class and a success value
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category": {"type":"history", "id": 4}}'`
```
{
  "question": {
    "answer": "Muhammad Ali", 
    "category": 4, 
    "difficulty": 1, 
    "id": 9, 
    "question": "What boxer's original name is Cassius Clay?"
  }, 
  "success": true
}
```
