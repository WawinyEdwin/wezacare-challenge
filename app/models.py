from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=225, null=False, unique=True)
    password = models.CharField(max_length=225, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Question(models.Model):
    question_text = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_email = models.EmailField(max_length=225, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Answer(models.Model):
    answer_text = models.CharField(max_length=500)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_email = models.EmailField(max_length=225, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
