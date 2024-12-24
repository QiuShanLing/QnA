# QnA Project

This project is a QnA (Questions and Answers) web application. It consists of a backend built with FastAPI and a frontend that interacts with the backend.

## Features

- Create, read, update, and search questions.
- Mark questions with answers.
- CORS configuration to allow frontend interaction.

## Backend

The backend is implemented using FastAPI and SQLAlchemy for database interactions.

### Endpoints

- `GET /questions/`: Retrieve all questions.
- `GET /questions/search/`: Search questions by keyword.
- `POST /questions/`: Create a new question.
- `GET /questions/{question_id}`: Retrieve a specific question by ID.
- `PUT /questions/{question_id}/answer`: Update the answer for a specific question.

### Running the Backend

1. Install dependencies:
    ```bash
    pip install fastapi sqlalchemy uvicorn
    ```

2. Start the server:
    ```bash
    uvicorn main:app --reload
    ```

## Frontend

The frontend interacts with the backend through the defined API endpoints. Ensure the frontend is configured to communicate with the backend server running on `http://localhost:8080`.

## Usage

1. Start the backend server.
2. Open the frontend application.
3. Use the frontend interface to create, read, update, and search questions.

## License

This project is licensed under the MIT License.
