# Student Task Management System

## Project Description

The Student Task Management System is a small dynamic web application developed using Python and Flask. It helps students manage their academic tasks by allowing them to add, complete, delete, search, filter, and sort tasks.

The application uses server-generated HTML pages and provides REST-style JSON endpoints for accessing task information.

The project also demonstrates Cloud Computing and DevOps concepts such as Git, GitHub, GitHub Actions, Docker, CI/CD, automated testing, linting, and deployment using Render.

---

## Features

- Add new student tasks
- Task validation
- Mark tasks as completed
- Delete tasks
- Search tasks by task name or subject
- Filter tasks by status and priority
- Sort tasks by deadline
- Sort tasks by priority
- Display task statistics
- JSON API for task data
- Health check endpoint
- Commit ID displayed in the application footer
- Automated testing using pytest
- Code quality checking using flake8
- Docker containerization
- Automated CI/CD using GitHub Actions
- Automatic deployment to Render

---

## Technologies Used

- Python
- Flask
- HTML
- CSS
- Git
- GitHub
- GitHub Actions
- Docker
- Render
- pytest
- flake8
- Gunicorn

---

## Project Structure

```text
student-task-management-system/
│
├── app.py
├── test_app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .flake8
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── .github/
    └── workflows/
        └── ci-cd.yml