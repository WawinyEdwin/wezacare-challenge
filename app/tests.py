from django.urls import reverse
from django.test import TestCase, Client
from .models import User, Question, Answer
from .serializers import QuestionSerializer, UserSerializer, AnswerSerializer
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .auth import verify_user, sign_token
import json
from rest_framework.test import APIClient, APITestCase
import base64


# initialize the APIClient app
client = APIClient()


class CreateUserTest(APITestCase):
    """Test module for the creating a new user"""

    def setUp(self):
        self.valid_payload = {"email": "johndoe@gmail.com", "password": "123456"}
        self.invalid_payload = {"email": "", "password": "123456"}

    def test_create_valid_user(self):
        response = client.post(
            path="/auth/register/",
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        response = client.post(
            path="/auth/register/",
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginUserTest(APITestCase):
    """Test Module for User login"""

    def setUp(self):
        self.user_one = User.objects.create(
            email="johndoe@gmail.com", password=make_password("123456")
        )
        self.valid_payload = {
            "email": "johndoe@gmail.com",
            "password": "123456",
        }
        self.invalid_payload = {"email": "johndoe@gmail.com", "password": "1234567"}

    def test_login_valid_user(self):
        response = client.post(
            path="/auth/login/",
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_user(self):
        response = client.post(
            path="/auth/login/",
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetAllQuestionsTest(APITestCase):
    """Test Module for the  Question Model"""

    def setUp(self):
        self.author_one = User.objects.create(
            email="johndoe@gmail.com", password=make_password("123456")
        )
        Question.objects.create(
            question_text="What is your name?", author=self.author_one
        )
        Question.objects.create(
            question_text="What is your age?", author=self.author_one
        )

    def test_get_all_questions(self):
        response = client.get(path="/questions/")
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleQuestionTest(APITestCase):
    """Test module for retrieving a single question"""

    def setUp(self):
        self.author_one = User.objects.create(
            email="johndoe@gmail.com", password=make_password("123456")
        )
        self.quiz_one = Question.objects.create(
            question_text="What is your name?", author=self.author_one
        )

    def test_get_valid_single_question(self):
        url = reverse("question_detail", kwargs={"question_id": self.quiz_one.pk})
        response = client.get(url)
        question = Question.objects.get(pk=self.quiz_one.pk)
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

    def test_get_invalid_single_question(self):
        response = client.get(path="question_detail", kwargs={"question_id": 10})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteSingleQuestionTest(APITestCase):
    """Test Module for deleting a single question"""

    def setUp(self):
        self.author_one = User.objects.create(
            email="johndoe@gmail.com", password=make_password("123456")
        )
        self.token = sign_token(self.author_one)
        self.quiz_one = Question.objects.create(
            question_text="What is your age?", author=self.author_one
        )

    def test_delete_valid_question(self):
        url = reverse("question_detail", kwargs={"question_id": self.quiz_one.pk})
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_question(self):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        url = reverse("question_detail", kwargs={"question_id": 13})
        response = client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewQuestion(APITestCase):
    """Test module for creating a new question"""

    def setUp(self):
        self.author_one = User.objects.create(
            email="johndoe@gmail.com", password=make_password("123456")
        )
        self.token = sign_token(self.author_one)
        self.valid_payload = {
            "question_text": "What is your age?",
            "author": self.author_one.pk,
        }
        self.invalid_payload = {"question_text": " ", "author": ""}

    def test_create_valid_question(self):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.post(
            path="/questions/", data=json.dumps(self.valid_payload), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_question(self):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.post(
            path="/questions/", data=json.dumps(self.invalid_payload), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateAnswerTest(APITestCase):
    """Test Module for the creation of answer"""

    def setUp(self):
        self.author_one = User.objects.create(
            email="johndoe@gmail.com", password=make_password("123456")
        )
        self.token = sign_token(self.author_one)
        self.quiz_one = Question.objects.create(
            question_text="What is your name?", author=self.author_one
        )
        self.valid_payload = {"answer_text": "Googlo"}
        self.invalid_payload = {"answer_text": ""}

    def test_create_valid_answer(self):
        url = reverse("answers", kwargs={"question_id": self.quiz_one.pk})
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.post(
            path=url, data=json.dumps(self.valid_payload), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_answer(self):
        url = reverse("answers", kwargs={"question_id": self.quiz_one.pk})
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.post(
            path=url, data=json.dumps(self.invalid_payload), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateAnswerTest(APITestCase):
    """Test Module for the creation of answer"""

    def setUp(self):
        self.author_one = User.objects.create(
            email="johndoe@gmail.com", password=make_password("123456")
        )
        self.token = sign_token(self.author_one)
        self.quiz_one = Question.objects.create(
            question_text="What is your name?", author=self.author_one
        )
        self.answer_one = Answer.objects.create(
            answer_text="Gogo", author=self.author_one, question=self.quiz_one
        )
        self.valid_payload = {"answer": "Googlo"}
        self.invalid_payload = {"answer": ""}

    def test_update_valid_answer(self):
        url = reverse("answer_detail", args=[self.quiz_one.pk, self.answer_one.pk])
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.put(
            path=url,
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_invalid_answer(self):
        url = reverse("answer_detail", args=[self.quiz_one.pk, self.answer_one.pk])
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.post(
            path=url, data=json.dumps(self.invalid_payload), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteAnswerTest(TestCase):
    """Test Module for the deletion of an answer"""

    def setUp(self):
        self.author_one = User.objects.create(
            email="johndoe@gmail.com", password=make_password("123456")
        )
        self.token = sign_token(self.author_one)

        self.quiz_one = Question.objects.create(
            question_text="What is your name?", author=self.author_one
        )
        self.answer_one = Answer.objects.create(
            answer_text="Gogo", author=self.author_one, question=self.quiz_one
        )

    def test_delete_valid_answer(self):
        url = reverse("answer_detail", args=[self.quiz_one.pk, self.answer_one.pk])
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_answer(self):
        url = reverse("answer_detail", args=[self.quiz_one.pk, 13])
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
