from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from authentication.models import User
from .utils import random_variant


CHOICE_FOR_SUBJECT = (
    (1, 'Math'),
    (2, 'English'),
    (3, 'Physics'),
)

CHOICE_FOR_VARIANT = (
    (1, 'Birinchi variant'),
    (2, 'Ikkinchi variant'),
    (3, 'Uchinchi variant'),
)

CHOICE_FOR_CHOICE = (
    (1, 'A'),
    (2, 'B'),
    (3, 'C'),
    (3, 'D'),
)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class QuestionType(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Subject(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.IntegerField(choices=CHOICE_FOR_SUBJECT)

    def __str__(self):
        return f'{self.get_name_display()}'


class DefaultExam(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    duration = models.PositiveIntegerField(default=60, help_text='Only minutes')
    questions = models.PositiveIntegerField(default=30)
    limit_for_candidates = models.PositiveIntegerField(default=30)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    mandat_data = models.DateTimeField()

    def __str__(self):
        return f'{self.name}'


class Exam(BaseModel):
    default = models.ForeignKey(DefaultExam, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    variant = models.PositiveIntegerField(choices=CHOICE_FOR_VARIANT, default=random_variant)

    def __str__(self):
        return f'{self.subject}'


class Question(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    variant = models.IntegerField(choices=CHOICE_FOR_VARIANT)
    question = models.TextField()
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    A = models.CharField(max_length=100, blank=True)
    B = models.CharField(max_length=100, blank=True)
    C = models.CharField(max_length=100, blank=True)
    D = models.CharField(max_length=100, blank=True)
    correct_answer = models.IntegerField(choices=CHOICE_FOR_CHOICE, blank=True, null=True)
    open_question_answer = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.id}'


class Result(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    status_for_checked_or_unchecked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}'


class Answer(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    true_or_false = models.BooleanField(default=False)
    status_for_checked_or_unchecked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}'


@receiver(post_save, sender=Answer)
def post_save_for_answer(sender, instance, created, **kwargs):
    questions = Question.objects.filter(subject=instance.question.subject,
                                        variant=instance.question.variant,
                                        question_type=2).count()

    answers = Answer.objects.filter(user=instance.user, question_type=2, status_for_checked_or_unchecked=True).count()

    if answers == questions:
        correct_answers = Answer.objects.filter(user=instance.user, question_type=2, true_or_false=True).count()
        result = Result.objects.filter(user=instance.user).first()
        result.correct_answers += correct_answers
        result.status_for_checked_or_unchecked = True
        result.save()



