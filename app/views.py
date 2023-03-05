from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .auth import verify_user, sign_token
from .models import User, Answer, Question
from django.contrib.auth.hashers import make_password, check_password


@api_view(["POST"])
def register_user(request):
    """
    Grabs user registration info and stores it
    """
    if not request.data:
        return Response(
            {"message": "All fields required"}, status=status.HTTP_400_BAD_REQUEST
        )

    email = request.data["email"]
    password = request.data["password"]
    user = User(
        email=email,
        password=make_password(password),
    )
    user.save()
    return Response({"message": "Account Created"}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def login_user(request):
    """
    Grab user login info and authenticate them.
    """
    email = request.data["email"]
    password = request.data["password"]
    user = User.objects.get(email=email)
    if user is None:
        return Response(
            {"message": "This User Does Not Exist"}, status=status.HTTP_401_UNAUTHORIZED
        )

    if check_password(password, user.password):
        return Response(sign_token(user), status=status.HTTP_200_OK)
    return Response(
        {"message": "Incorrect Password"}, status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(["GET", "POST"])
def questions(request):
    """
    GET:
        Fetches all questions.

    POST:
        Posts a question.
    """
    if request.method == "GET":
        questions = Question.get_questions()
        return Response(questions, status=status.HTTP_200_OK)

    if request.method == "POST":
        auth = verify_user(authorization=request.META.get("HTTP_AUTHORIZATION"))
        if auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not request.data:
            return Response(
                {"message": "All fields required"}, status=status.HTTP_400_BAD_REQUEST
            )

        question_text = request.data["question"]
        question = Question(
            question_text=question_text,
            author=auth.id,
        )
        question.save()

        return Response({"message": "Question Posted"}, status=status.HTTP_201_CREATED)


@api_view(["GET", "DELETE"])
def question_detail(request, question_id):
    """
    GET:
        Fetch a specific question and its answers

    DELETE:
        Delete a question, only one who created the question can perform this operation

    Args:
       question_id (int): question unique id
    """
    if request.method == "GET":
        question = Question.get_single_question(question_id)
        return Response(question, status=status.HTTP_200_OK)

    if request.method == "DELETE":
        auth = verify_user(authorization=request.META.get("HTTP_AUTHORIZATION"))
        if auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        question = Question.objects.get(pk=question_id)
        if question.author != auth.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # delete the question
        question.delete()
        return Response(question, status=status.HTTP_200_OK)


@api_view(["POST"])
def answers(request, question_id):
    """
    Post an answer to a question

    Args:
        question_id (int): question unique id
    """
    auth = verify_user(authorization=request.META.get("HTTP_AUTHORIZATION"))
    if auth is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if not request.data:
        return Response(
            {"message": "All fields required"}, status=status.HTTP_400_BAD_REQUEST
        )

    answer_text = request.data["answer"]
    answer = Answer(answer_text=answer_text, author=auth.id, question=question_id)
    answer.save()

    return Response({"message": "Posted an answer"}, status=status.HTTP_201_CREATED)


@api_view(["PUT", "DELETE"])
def answer_detail(request, question_id, answer_id):
    """
    PUT:
        Update an answer, only the answer author can

    DELETE:
        Delete an answer, only the answer author can

    Args:
        question_id (int): question unique id
        answer_id (int): answer unique id
    """
    auth = verify_user(authorization=request.META.get("HTTP_AUTHORIZATION"))
    if auth is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    ans = Answer.objects.get(pk=answer_id)
    if ans.author != auth.id:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "PUT":
        answer_update = request.data["answer"]
        answer = Answer(answer_text=answer_update)
        answer.save()
        return Response(status=status.HTTP_200_OK)

    if request.method == "DELETE":
        ans.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def api(request):
    return Response({"message": "API is running...."}, status=status.HTTP_200_OK)
