
# JWT
    We creating guest JWT token, because we don`t have user registration.
    Token payload contain two additional fields: guest_id and guest

# Pagination
    - Comments . Paginated with PageNumber pagination. Default value 25.
    - Replies. Paginated with LimitOffset pagination. Default value 10

# Input validation
    - email. max length: 254 symbols. Email format.
    - text. Max length: 1500 symbols, min length: 1 symbol. Allowed html tags, attributes(TODO)
    - username. Max length: 60 symbols, min length: 3 symbols. Only latin letters and digits
    - homepage. Max length: 200 symbols. URL format.

# Environment variables
## required
    SECRET_KEY - Django application secret key. String value. Example: 'random str'
    REDIS_HOST - Redis host. Example: 'localhost'
    DB_NAME - Postgresql database name. Example: 'test_db'
    DB_HOST - Postgresql database host. Example: 'localhost
    DB_PORT - Postgresql database port. Example: 5432
    DB_USER - Postgresql database user. Example: 'root'
    DB_PASSWORD - Postgresql database password. Example: 'pass123'
## other
    BASE_URL - Base server URL. Default: 'http://localhost:8000'
    REDIS_PORT - Redis port. Example: 6380. Default: 6379
    ACCESS_TOKEN_LIFETIME - Lifetime of JWT access token
    REFRESH_TOKEN_LIFETIME - Lifetime of JWT refresh token


# How to run application
## 1. Install Postgresql
### Ubuntu
    1. Update index
        sudo apt update
    2. Install Postgresql
        sudo apt install postgresql postgresql-contrib
    3. Check that service is running
        sudo systemctl status postgresql
### Windows
    1. Install from official site (https://www.postgresql.org/download/windows/)
## 2. Install Python
### Ubuntu
    1. Add PPA repository
        sudo apt update
        sudo apt upgrade
        sudo add-apt-repository ppa:deadsnakes/ppa
        sudo apt update
    2. Install python
        sudo apt install python3.10 python3.10-venv python3.10-dev
    3. Check
        python3.10 --version
### Windows
    1. Install from official site (https://www.python.org/downloads/release/python-3100/)
## 3. Install dependencies
    1. Create virtual environment
        python3.10 -m venv venv
    2. activate environment
        Ubuntu: source venv/bin/activate
        Windows: venv\Scripts\activate
    3. install dependencies
        cd backend
        pip install -r requirements.txt
## 4. Set environment variables
        set REQUIRED env variables in terminal or in .env file inside backend folder
## 5. Run application
        While in virtual environment and inside backend folder:
            python manage.py runserver - run application
            celery -A conf worker -l info - run celery worker