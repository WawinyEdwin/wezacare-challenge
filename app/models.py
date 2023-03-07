from django.db import models

# Create your models here.


class User(models.Model):
    email = models.EmailField(max_length=225, null=False, unique=True)
    password = models.CharField(max_length=225, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text

    class Meta:
        ordering = ["created_at"]


class Answer(models.Model):
    answer_text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer_text

    class Meta:
        ordering = ["created_at"]
