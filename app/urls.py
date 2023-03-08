from django.urls import path
from . import views

urlpatterns = [
    path("", views.api),
    path("auth/register/", views.register_user, name="register_user"),
    path("auth/login/", views.login_user, name="login_user"),
    path("questions/", views.questions, name="questions"),
    path("questions/<int:question_id>/", views.question_detail, name="question_detail"),
    path("questions/<int:question_id>/answers/", views.answers, name="answers"),
    path(
        "questions/<int:question_id>/answers/<int:answer_id>/",
        views.answer_detail,
        name="answer_detail",
    ),
]
