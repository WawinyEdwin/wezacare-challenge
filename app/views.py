from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import QuestionSerializer, UserSerializer, AnswerSerializer
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
    data = {"email": request.data["email"], "password": request.data["password"]}

    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "account created"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_user(request):
    """
    Grab user login info and authenticate them.
    """
    email = request.data["email"]
    password = request.data["password"]
    user = User.objects.filter(email=email).first()
    if user is None:
        return Response(
            {"message": "This User Does Not Exist"}, status=status.HTTP_401_UNAUTHORIZED
        )

    if check_password(password, user.password):
        return Response({"token": sign_token(user)}, status=status.HTTP_200_OK)
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
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "POST":
        auth = verify_user(authorization=request.META.get("HTTP_AUTHORIZATION"))
        if auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        author = User.objects.get(pk=auth.get("user_id"))
        data = {"question_text": request.data["question_text"], "author": author.pk}
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Question Posted"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    try:
        question = Question.objects.get(pk=question_id)
        answers = question.answers.all()
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = QuestionSerializer(question)
        answer_serializer = AnswerSerializer(answers, many=True)
        return Response(
            {"question": serializer.data, "answers": answer_serializer.data},
            status=status.HTTP_200_OK,
        )

    if request.method == "DELETE":
        serializer = QuestionSerializer(question)
        auth = verify_user(authorization=request.META.get("HTTP_AUTHORIZATION"))
        if auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if serializer.data["author"] != auth["user_id"]:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # delete the question
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    data = {
        "answer_text": request.data["answer_text"],
        "question": question_id,
        "author": auth.get("user_id"),
    }
    serializer = AnswerSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Answer Posted"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    try:
        ans = Answer.objects.get(pk=answer_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AnswerSerializer(ans)
    if serializer.data["author"] != auth["user_id"]:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "PUT":
        serializer = AnswerSerializer(ans, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        ans.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def api(request):
    return Response({"message": "API is running...."}, status=status.HTTP_200_OK)
