from django.db import models

# Create your models here.


class User(models.Model):
    email = models.EmailField(max_length=225, null=False, unique=True)
    password = models.CharField(max_length=225, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.question_text

    def get_questions(self):
        return Question.objects.all()

    def get_single_question(self, question_id):
        return Question.objects.filter(pk=question_id)


class Answer(models.Model):
    answer_text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer_text
    
    class Meta:
        ordering = ["created_at"]
    
