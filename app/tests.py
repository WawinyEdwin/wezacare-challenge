import base64
import json

from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .auth import sign_token
from .models import Answer, Question, User
from .serializers import AnswerSerializer, QuestionSerializer, UserSerializer


class UserTest(APITestCase):
    """Test module for the User Model"""

    def setUp(self):
        self.user = User.objects.create(
            email="mayangelou@mail.com", password=make_password("maya123")
        )
        self.login_payload = {"email": "mayangelou@mail.com", "password": "maya123"}
        self.valid_payload = {"email": "johndoe@gmail.com", "password": "123456"}
        self.invalid_payload = {"email": "", "password": "123456"}

    def test_create_valid_user(self):
        response = self.client.post(
            path="/auth/register/",
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        response = self.client.post(
            path="/auth/register/",
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_valid_user(self):
        response = self.client.post(
            path="/auth/login/",
            data=json.dumps(self.login_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_user(self):
        response = self.client.post(
            path="/auth/login/",
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class QuestionTest(APITestCase):
    """Test Module for the  Question Model"""

    def setUp(self):
        self.user = User.objects.create(
            email="johndol@gmail.com", password=make_password("123456")
        )
        self.quiz = Question.objects.create(
            question_text="What is your name?",
            author=self.user,
            author_email=self.user.email,
        )
        self.quiz_two = Question.objects.create(
            question_text="What is your age?",
            author=self.user,
            author_email=self.user.email,
        )
        self.token = sign_token(self.user)
        self.api_authentication()
        self.valid_payload = {"question_text": "What is your age?"}
        self.invalid_payload = {"question_text": " "}

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_create_valid_question(self):
        response = self.client.post(
            path="/questions/",
            data=self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_question(self):
        response = self.client.post(
            path="/questions/",
            data=self.invalid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_questions(self):
        response = self.client.get(path="/questions/")
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_question(self):
        url = reverse("question_detail", kwargs={"question_id": self.quiz.pk})
        response = self.client.get(url)
        question = Question.objects.get(pk=self.quiz.pk)
        answers = question.answers.all()
        serializer = QuestionSerializer(question)
        answer_serializer = AnswerSerializer(answers, many=True)

        self.assertEqual(
            {
                "question": response.data["question"],
                "answers": response.data["answers"],
            },
            {
                "question": serializer.data,
                "answers": answer_serializer.data,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_valid_question(self):
        url = reverse("question_detail", kwargs={"question_id": self.quiz.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AnswerTest(APITestCase):
    """Test Module for the Answer Model"""

    def setUp(self):
        self.user = User.objects.create(email="johndol@gmail.com", password="123456")
        self.quiz = Question.objects.create(
            question_text="What is your name?",
            author=self.user,
            author_email=self.user.email,
        )
        self.answer = Answer.objects.create(
            answer_text="A good answer", author=self.user, question=self.quiz
        )
        self.token = sign_token(self.user)
        self.api_authentication()
        self.valid_payload = {"answer_text": "Googlo"}
        self.invalid_payload = {"answer_text": " "}

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_create_valid_answer(self):
        url = reverse("answers", kwargs={"question_id": self.quiz.pk})
        response = self.client.post(path=url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_answer(self):
        url = reverse("answers", kwargs={"question_id": self.quiz.pk})
        response = self.client.post(path=url, data=self.invalid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid_answer(self):
        url = reverse("answer_detail", args=[self.quiz.pk, self.answer.pk])
        response = self.client.put(
            path=url,
            data={
                "answer_text": "Googlo",
                "author": self.user.pk,
                "question": self.quiz.pk,
                "author_email": self.user.email,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_valid_answer(self):
        url = reverse("answer_detail", args=[self.quiz.pk, self.answer.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
