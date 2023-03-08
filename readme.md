## Kevin's Service

### Introduction

This backend service serves frontend clients.

### Kevin's Service Features

- Users can create an account as well as log in to the platform
- Users can post questions on the platform
- Users can answer questions posted only by others on the platform
- Given an ID, users can retrieve a particular question with that ID, along with the answers to the question.
- User can view all the questions that they have ever asked on the platform

### Installation Guide

- Clone this repository [here](https://github.com/LL04-Finance-Dowell/100018-dowellWorkflowAi-testing.git).
- The `main` branch is the most stable branch at any given time, ensure you're working from it.
- Run `pip install -r requirements.txt` to install dependencies.

### Usage

- Run `python manage.py runserver 8001` to start the application.
- Connect to the API using Postman on port 8001.

### API Authorization

- Authorization `Bearer Token`

### API Endpoints

| HTTP Verbs | Endpoints                                     | Action                                      |
| ---------- | --------------------------------------------- | ------------------------------------------- |
| POST       | /auth/login/                                  | To authenticates a user                     |
| POST       | /auth/register/                               | To create an account for a user             |
| GET        | /questions/                                   | To retrieve all questions                   |
| POST       | /questions/                                   | To create a question                        |
| GET        | /questions/<question_id>/                     | To retrieve a single question+ its answers. |
| DELETE     | /questions/<question_id>/                     | To delete a single question+ its answers.   |
| GET        | /questions/<question_id>/answers/             | To post an answer for a question.           |
| PUT        | /questions/<question_id>/answers/<answer_id>/ | To update an answer for a question.         |
| DELETE     | /questions/<question_id>/answers/<answer_id>/ | To delete an answer to a question.          |

---

### API Documentation 

[Kevin-Service](https://documenter.getpostman.com/view/17474568/2s93JqSR4c)


### Technologies Used

- [Python](https://nodejs.org/) is a programming language that lets you work more quickly and integrate your systems
  more effectively.
- [Django](https://www.djangoproject.com/) is a high-level Python web framework that encourages rapid development and
  clean, pragmatic design.
- [Django Rest Framework](https://www.django-rest-framework.org/) Django REST framework is a powerful and flexible
  toolkit for building Web APIs.
- [SQLite](https://www.sqlite.org/) SQLite is an in-process library that implements a self-contained, serverless, zero-configuration, transactional SQL database engine
