# Sparrow - Messaging App

## Overview
Sparrow is a Django-based messaging application that provides user authentication, room management, and messaging features. It uses Django REST Framework for API endpoints and JWT for authentication.

## Features
- User registration and authentication using JWT
- Room management (create, join, leave rooms)
- Member management within rooms
- RESTful API endpoints for all features
- Swagger and Redoc documentation for API exploration

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- PostgreSQL

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd sparrow
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database:
   - Update `sparrow/settings.py` with your PostgreSQL credentials.
   - Run migrations:
     ```bash
     python manage.py migrate
     ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation
- Swagger UI: `http://localhost:8000/swagger/`
- Redoc: `http://localhost:8000/redoc/`

## Usage Examples

### Register a User
```bash
curl -X POST http://localhost:8000/tokens/register/ -H "Content-Type: application/json" -d '{"title":"user1","email":"user1@example.com","password":"password123","first_name":"John","last_name":"Doe"}'
```

### Obtain JWT Token
```bash
curl -X POST http://localhost:8000/tokens/ -H "Content-Type: application/json" -d '{"email":"user1@example.com","password":"password123"}'
```

### Create a Room
```bash
curl -X POST http://localhost:8000/apiv1/rooms/ -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json" -d '{"name":"General"}'
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.
