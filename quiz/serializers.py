from .models import Subject, Question, Answer, Result, DefaultExam
from rest_framework import serializers


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['name'] = instance.get_name_display()
        return data


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'subject', 'variant', 'question', 'A', 'B', 'C', 'D']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['subject'] = instance.subject.get_name_display()
        data['variant'] = instance.variant
        return data


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'user', 'question', 'question_type', 'answer', ]


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['id', 'user', 'exam', 'total_questions', 'correct_answers', ]


class DefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultExam
        fields = ['id', 'user', 'name', 'subject', 'duration', 'questions', 'limit_for_candidates',
                  'start_time', 'end_time', 'mandat_data']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = instance.user.username
        data['subject'] = instance.subject.get_name_display()

        return data


class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'user', 'subject', 'variant', 'question', 'question_type',
                  'A', 'B', 'C', 'D', 'correct_answer', 'open_question_answer', ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = instance.user.username
        data['subject'] = instance.subject.get_name_display()
        data['variant'] = instance.variant
        data['question_type'] = instance.question_type.name
        data['correct_answer'] = instance.correct_answer
        return data
