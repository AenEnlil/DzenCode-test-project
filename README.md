# Description:
    Test task for 'DZEN code' company
# Main functionality:
    - Main comments creation and abillity to unlimitedly reply them and the other answers
    - Abillity to go to between and replies
    - Main comments sorting by username, email and creation date
    - Main comments and replies pagination
    - Automatical comment update through Websockets
    - Abillity to attach image or file to comment
    - JWT Authentication
    - Events and Task queue
    - Page caching
# Technologies:
    - Vue: 3.5.13
    - Python: 3.10
    - Django: 5.2
    - Postgresql: 14.7
    - Redis: 8.0
    - Celery: 5.5.2
    - Nginx
    - Docker 27.3.1
    - docker-compose 1.29.2
# Project structure:
    ├── frontend/     # Client application
    ├── backend/      # Server application
    ├── deployment/   # Docker
# How to run application
 ## with Docker
- check deploy README (./deployment/README.md)
 ## manual
- Install and run frontend application(./frontend.README.md)
- Install and run backend application(./backend.README.md)
 