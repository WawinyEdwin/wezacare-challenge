from django.urls import path
from . import views

urlpatterns = [
    path("", views.api),
    path("auth/register/", views.register_user),
    path("auth/login/", views.login_user),
    path("questions/", views.questions),
    path("questions/<int:question_id>/", views.question_detail),
    path("questions/<int:question_id>/answers", views.answers),
    path("questions/<int:question_id>/answers/<int:answer_id>/", views.answer_detail),
]
