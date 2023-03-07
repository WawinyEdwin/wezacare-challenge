from django.urls import reverse
from django.test import TestCase, Client
from .models import User, Question, Answer
from .serializers import QuestionSerializer, UserSerializer, AnswerSerializer
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .auth import verify_user, sign_token
import json
import base64


# initialize the APIClient app
client = Client()


# class CreateUserTest(TestCase):
#     """Test module for the creating a new user"""

#     def setUp(self):
#         self.valid_payload = {"email": "johndoe@gmail.com", "password": "123456"}
#         self.invalid_payload = {"email": "", "password": "123456"}

#     def test_create_valid_user(self):
#         response = client.post(
#             reverse("register_user"),
#             data=json.dumps(self.valid_payload),
#             content_type="application/json",
#         )

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_create_invalid_user(self):
#         response = client.post(
#             reverse("register_user"),
#             data=json.dumps(self.invalid_payload),
#             content_type="application/json",
#         )

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class LoginUserTest(TestCase):
#     """Test Module for User login"""

#     def setUp(self):
#         self.user_one = User.objects.create(
#             email="johndoe@gmail.com", password=make_password("123456")
#         )
#         self.valid_payload = {
#             "email": "johndoe@gmail.com",
#             "password": "123456",
#         }
#         self.invalid_payload = {"email": "johndoe@gmail.com", "password": "1234567"}

#     def test_login_valid_user(self):
#         response = client.post(
#             reverse("login_user"),
#             data=json.dumps(self.valid_payload),
#             content_type="application/json",
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_login_invalid_user(self):
#         response = client.post(
#             reverse("login_user"),
#             data=json.dumps(self.invalid_payload),
#             content_type="application/json",
#         )
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateNewQuestion(TestCase):
    """Test module for creating a new question"""

    def setUp(self):
        self.author_one = User.objects.create(
            email="johndoe@gmail.com", password=make_password("123456")
        )
        self.auth_headers = {
            "HTTP_AUTHORIZATION": "Bearer " + sign_token(self.author_one),
        }
        self.valid_payload = {
            "question_text": "What is your age?",
        }
        self.invalid_payload = {
            "question_text": " ",
        }

    def test_create_valid_question(self):
        response = client.post(
            reverse("questions"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
            **self.auth_headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_question(self):
        response = client.post(
            reverse("questions"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
            **self.auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class GetAllQuestionsTest(TestCase):
#     """Test Module for the  Question Model"""

#     def setUp(self):
#         self.author_one = User.objects.create(
#             email="johndoe@gmail.com", password=make_password("123456")
#         )
#         Question.objects.create(
#             question_text="What is your name?", author=self.author_one
#         )
#         Question.objects.create(
#             question_text="What is your age?", author=self.author_one
#         )

#     def test_get_all_questions(self):
#         response = client.get(reverse("questions"))
#         questions = Question.objects.all()
#         serializer = QuestionSerializer(questions, many=True)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class GetSingleQuestionTest(TestCase):
#     """Test module for retrieving a single question"""

#     def setUp(self):
#         self.author_one = User.objects.create(
#             email="johndoe@gmail.com", password=make_password("123456")
#         )
#         self.quiz_one = Question.objects.create(
#             question_text="What is your name?", author=self.author_one
#         )

#     def test_get_valid_single_question(self):
#         response = client.get(
#             reverse("question_detail", kwargs={"question_id": self.quiz_one.pk})
#         )
#         question = Question.objects.get(pk=self.quiz_one.pk)
#         serializer = QuestionSerializer(question)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_invalid_single_question(self):
#         response = client.get(reverse("question_detail", kwargs={"question_id": 10}))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# class DeleteSingleQuestionTest(TestCase):
#     """Test Module for deleting a single question"""

#     def setUp(self):
#         self.author_one = User.objects.create(
#             email="johndoe@gmail.com", password=make_password("123456")
#         )
#         self.auth_headers = {
#             "HTTP_AUTHORIZATION": "Bearer " + sign_token(self.author_one),
#         }
#         self.author_two = User.objects.create(
#             email="john@gmail.com", password=make_password("1234567")
#         )
#         self.quiz_one = Question.objects.create(
#             question_text="What is your age?", author=self.author_one
#         )

#     def test_delete_valid_question(self):
#         response = client.delete(
#             reverse(
#                 "question_detail", kwargs={"question_id": self.quiz_one.pk}, **self.auth_headers
#             ),
#         )
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     def test_delete_invalid_question(self):
#         client.credentials(self.auth_headers)
#         response = client.delete(
#             reverse("question_detail", kwargs={"question_id": 15}),
#         )
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# class CreateAnswerTest(TestCase):
#     """Test Module for the creation of answer"""

#     def setUp(self):
#         self.author_one = User.objects.create(
#             email="johndoe@gmail.com", password=make_password("123456")
#         )
#         self.auth_headers = {
#             "HTTP_AUTHORIZATION": "Bearer " + sign_token(self.author_one),
#         }
#         self.quiz_one = Question.objects.create(
#             question_text="What is your name?", author=self.author_one
#         )
#         self.valid_payload = {
#             "answer": "Googlo",
#             "author": self.author_one,
#             "question": self.quiz_one,
#         }
#         self.invalid_payload = {"answer": ""}

#     def test_create_valid_answer(self):
#         client.credentials(self.auth_headers)
#         response = client.post(
#             reverse("answers"),
#             data=json.dumps(self.valid_payload),
#             content_type="application/json",
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_create_invalid_answer(self):
#         client.credentials(self.auth_headers)
#         response = client.post(
#             reverse("answers"),
#             data=json.dumps(self.invalid_payload),
#             content_type="application/json",
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class UpdateAnswerTest(TestCase):
#     """Test Module for the creation of answer"""

#     def setUp(self):
#         self.author_one = User.objects.create(
#             email="johndoe@gmail.com", password=make_password("123456")
#         )
#         self.auth_headers = {
#             "HTTP_AUTHORIZATION": "Bearer " + sign_token(self.author_one),
#         }
#         self.quiz_one = Question.objects.create(
#             question_text="What is your name?", author=self.author_one
#         )
#         self.valid_payload = {"answer": "Googlo"}
#         self.invalid_payload = {"answer": ""}

#     def test_update_valid_answer(self):
#         client.credentials(self.auth_headers)
#         response = client.put(
#             reverse("answers"),
#             data=json.dumps(self.valid_payload),
#             content_type="application/json",
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_update_invalid_answer(self):
#         client.credentials(self.auth_headers)
#         response = client.post(
#             reverse("answers"),
#             data=json.dumps(self.invalid_payload),
#             content_type="application/json",
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class DeleteAnswerTest(TestCase):
#     """Test Module for the deletion of an answer"""

#     def setUp(self):
#         self.author_one = User.objects.create(
#             email="johndoe@gmail.com", password=make_password("123456")
#         )
#         self.auth_headers = {
#             "HTTP_AUTHORIZATION": "Bearer " + sign_token(self.author_one),
#         }
#         self.quiz_one = Question.objects.create(
#             question_text="What is your name?", author=self.author_one
#         )

#     def test_delete_valid_answer(self):
#         client.credentials(self.auth_headers)
#         response = client.delete(
#             reverse("answer_detail", kwargs={"pk": self.quiz_one.pk}),
#         )
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     def test_delete_invalid_question(self):
#         client.credentials(self.auth_headers)
#         response = client.delete(
#             reverse("answer_detail", kwargs={"pk": 15}),
#         )
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
