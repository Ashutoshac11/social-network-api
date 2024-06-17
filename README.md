# Social Networking Application API

This is a RESTful API for a social networking application built with Django and Django Rest Framework. The API allows users to sign up, log in, search for other users, send and manage friend requests, and list friends.

## Features

- User registration and authentication
- Search users by email or name
- Send, accept, and reject friend requests
- List friends and pending friend requests
- Rate limiting on sending friend requests

## Installation

### Prerequisites

- Python 3.8+
- Docker (optional, for containerization)
- PostgreSQL (or any database of your choice), default will be SQLite3 

### Step-by-Step Installation Guide

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Ashutoshac11/social-network-api.git
   cd social-network-api
   ```

2. **Create a Virtual Environment**

    ```python
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`


3. **Install Dependencies**
    
    ```python
    pip install -r requirements.txt

4. **Set-up Database/ leave it for the default SQLite3**
- Update the `DATABASES` setting in `social-network-api/settings.py` to match your database configuration.
- For example, for PostgreSQL:
    ```python
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yourdbname',
        'USER': 'yourdbuser',
        'PASSWORD': 'yourdbpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
    }

5. **Run Migrations**

    ```python
    python manage.py makemigrations
    python manage.py migrate

6. **Run the Development Server**

    ```python
    python manage.py runserver 

- The API will be available at `http://127.0.0.1:8000/`.



## Using Docker
1. **Build and Run Docker Containers**

- Make sure Docker is installed and running. Then, run the following command:

    ```bash
        docker-compose up --build
    
- The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints
### Authentication
- Signup: POST `/api/signup/`
- Login: POST `/api/login/`

### User Search
- Search Users: GET `/api/users/search/?q=keyword`

### Friend Requests
- Send Friend Request: POST `/api/request/`
- Accept Friend Request: POST `/api/friend-request/<id>/accept/`
- Reject Friend Request: POST `/api/friend-request/<id>/reject/`
- List Pending Friend Requests: GET `/api/friend-requests/`

### Friends
- List Friends: GET `/api/friends/`

## Postman Collection

- A Postman collection is included in the repository for testing the API endpoints. Import the `social-network-api.postman_collection.json` file into Postman to get started.

## Contributing
- Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Explanation

1. **Project Description**: Briefly describes the purpose of the project.
2. **Features**: Lists the main features of the API.
3. **Installation**: Provides step-by-step instructions to set up the project locally.
4. **Using Docker**: Instructions for setting up the project using Docker.
5. **API Endpoints**: Lists the available API endpoints and their purposes.
6. **Postman Collection**: Mentions the included Postman collection for easy testing.
7. **Contributing**: Instructions for contributing to the project.





 
