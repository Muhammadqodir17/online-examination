import requests
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from datetime import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import (
    Subject,
    Question,
    Exam,
    DefaultExam,
    Result,
    Answer,
    User
)
from .serializers import (
    SubjectSerializer,
    QuestionSerializer,
    AnswerSerializer,
    ResultSerializer,
    DefaultSerializer,
    CreateQuestionSerializer
)

BOT_ID = settings.BOT_ID
CHAT_ID = settings.CHAT_ID
TELEGRAM_API_URL = settings.TELEGRAM_API_URL


class SubjectViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get all subjects",
        operation_summary="Get all subjects",
        responses={
            200: SubjectSerializer(),
            404: "Not Found"
        },
        tags=['quiz']
    )
    def get_all(self, request, *args, **kwargs):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Choose Subject",
        operation_summary="Choose Subject",
        responses={
            404: "Not Found"
        },
        tags=['quiz']
    )
    def choose_subjects(self, request, *args, **kwargs):
        user = request.user
        subjects = Subject.objects.filter(id=kwargs['pk']).first()

        if subjects is None:
            return Response(data={'message': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)

        default = DefaultExam.objects.filter(subject=subjects).first()

        if default is None:
            return Response(data={'error': 'Default exam not found'}, status=status.HTTP_400_BAD_REQUEST)

        exist_exam = Exam.objects.filter(user=user).first()

        if default.end_time < datetime.now():
            return Response(data={'message': 'The exam has already ended'})

        elif default.start_time <= datetime.now():
            return Response(data={'message': 'The exam has already started'})

        if exist_exam is not None and default.start_time > datetime.now():
            return Response(data={'message': f'You have already chosen {exist_exam.subject} subject, '
                                             f'your exam will be start {default.start_time} '
                                             f'and your attendance id: {exist_exam.id}'},
                            status=status.HTTP_400_BAD_REQUEST)

        obj = Exam.objects.create(default=default, user=user, subject_id=kwargs['pk'])
        candidates = Exam.objects.filter(subject_id=kwargs['pk']).count()

        if candidates > default.limit_for_candidates:
            return Response(data={'message': 'The places have already been filled'})
        else:
            obj.save()

        return Response(data={'message': f'Your exam will be start {default.start_time} '
                                         f'and end {default.end_time}, '
                                         f'you have {default.duration} minutes '
                                         f'and {default.questions} questions, '
                                         f'your variant {obj.variant}, '
                                         f'limit for attendance: {default.limit_for_candidates}, '
                                         f'you have to enter the exam {default.start_time}, '
                                         f'here is your attendance id: {obj.id}'})

    @swagger_auto_schema(
        operation_description="Start Exam",
        operation_summary="Start Exam",
        tags=['quiz']
    )
    def start_test(self, request, *args, **kwargs):
        user = request.user

        exam = Exam.objects.filter(id=kwargs['pk']).first()

        if exam is None:
            return Response(data={'message': 'Invalid id'}, status=status.HTTP_404_NOT_FOUND)

        default = DefaultExam.objects.filter(subject=exam.subject).first()

        if default is None:
            return Response(data={'error': 'Default exam not found'}, status=status.HTTP_400_BAD_REQUEST)

        questions = Question.objects.filter(subject=exam.subject, variant=exam.variant)
        serializer = QuestionSerializer(questions, many=True)

        if default.start_time > datetime.now():
            return Response(data={'message': f'The exam will start {default.start_time}'})

        exist_result = Result.objects.filter(user=user).first()
        if exist_result is not None:
            return Response(data={'message': f'Test started {exam.default.start_time}, '
                                             f'test will end {exam.default.end_time}, '
                                             f'you have {exam.default.questions} questions, '
                                             f'your variant is {exam.variant}, '
                                             f'answer_sheet_id: {exist_result.id}, '
                                             f'here is questions: {serializer.data}'},
                            status=status.HTTP_200_OK)
        result = Result.objects.create(user=user, exam_id=kwargs['pk'])
        result.save()

        return Response(data={'message': f'Test started {exam.default.start_time}, '
                                         f'test will end {exam.default.end_time}, '
                                         f'you have {exam.default.questions} questions, '
                                         f'your variant is {exam.variant}, '
                                         f'answer_sheet_id: {result.id}, '
                                         f'here is questions: {serializer.data}'},
                        status=status.HTTP_200_OK
                        )

    @swagger_auto_schema(
        operation_description="Answer the question",
        operation_summary="Answer the question",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'question': openapi.Schema(type=openapi.TYPE_INTEGER, description='test name'),
                'question_type': openapi.Schema(type=openapi.TYPE_INTEGER, description='duration'),
                'answer': openapi.Schema(type=openapi.TYPE_STRING, description='questions'),
            },
            required=['question', 'question_type', 'answer']
        ),
        tags=['quiz'],
    )
    def answer(self, request, *args, **kwargs):
        user = request.user

        request.data['user'] = user.id
        serializer = AnswerSerializer(data=request.data)

        if serializer.is_valid():
            answer_sheet = Answer.objects.filter(user=user, question_id=request.data['question']).first()
            result = Result.objects.filter(id=kwargs['pk']).first()
            question = Question.objects.filter(id=request.data['question']).first()

            serializer.validated_data['user'] = user
            if result is None:
                return Response(data={'message': 'Invalid answer sheet id'}, status=status.HTTP_404_NOT_FOUND)

            default = DefaultExam.objects.filter(subject=result.exam.subject).first()

            if default.end_time == datetime.now():
                return Response(data={'message': 'The exam ended, '
                                                 f'You can see your result {default.mandat_data}'},
                                status=status.HTTP_200_OK)

            if result.total_questions == default.questions:
                return Response(data={'message': f'You answered all the questions, '
                                                 f'You can see your result {default.mandat_data}'})

            if answer_sheet is not None:
                return Response(data={'message': 'You have already answered this question'},
                                status=status.HTTP_400_BAD_REQUEST)

            if question.question_type.id != request.data['question_type']:
                return Response(data={'error': f'This question type is {question.question_type.id}'}, status=status.HTTP_400_BAD_REQUEST)

            if (request.data['question_type'] == 1
                    and int(request.data['answer']) > 4):
                return Response(data={'error': 'You have to pick for 1 "A", 2 "B", 3 "C", 4 "D" '
                                               'and it has to be int(digit)'},
                                status=status.HTTP_400_BAD_REQUEST)

            if question.correct_answer == int(request.data['answer']):
                result.correct_answers += 1
                result.total_questions += 1
                result.save()
            else:
                result.total_questions += 1
                result.save()
            serializer.save()

            if result.total_questions == default.questions:
                return Response(data={'message': f'You answered all the questions, '
                                                 f'You can see your result {default.mandat_data}'})

            return Response(data={'message': 'Answer accepted'}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Take your result",
        operation_summary="Take your result",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_STRING, description='test name'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='duration'),
            },
            required=['user', 'password']
        ),
        tags=['quiz'],
    )
    def mandat(self, request, *args, **kwargs):
        user = request.data['user']
        password = request.data['password']

        exist_user = User.objects.filter(username=user).first()
        if exist_user is None:
            return Response(data={'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if not exist_user.check_password(password):
            return Response(data={'error': 'Password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        exam = Exam.objects.filter(user__id=exist_user.id).first()

        if exam is None:
            return Response(data={'error': 'Exam not found'}, status=status.HTTP_404_NOT_FOUND)

        default = DefaultExam.objects.filter(subject=exam.subject).first()

        if datetime.now() < default.mandat_data:
            return Response(data={'message': f'Mandat"s data is {default.mandat_data}'},
                            status=status.HTTP_400_BAD_REQUEST)

        result = Result.objects.filter(user__username=exist_user.username, status_for_checked_or_unchecked=True).first()

        if result is None:
            return Response(data={'message': 'Your result is not ready yet'}, status=status.HTTP_400_BAD_REQUEST)

        message = (f"Project: Online Examination\n"
                   f"user:{result.user}\n"
                   f"exam:{result.exam}\n"
                   f"total_questions:{result.total_questions}\n"
                   f"correct_answers:{result.correct_answers}\n"
                   )

        response = requests.get(TELEGRAM_API_URL.format(BOT_ID, message, CHAT_ID))

        if response.status_code != 200:
            return Response(data={'message': 'Failed to send message to Telegram.'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(data={'message': 'Your result sent to telegram bot'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create Default Exam",
        operation_summary="Create Default Exam",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='test name'),
                'subject': openapi.Schema(type=openapi.TYPE_INTEGER, description='subject id'),
                'duration': openapi.Schema(type=openapi.TYPE_INTEGER, description='duration'),
                'questions': openapi.Schema(type=openapi.TYPE_INTEGER, description='questions'),
                'limit_for_candidate': openapi.Schema(type=openapi.TYPE_INTEGER, description='limit for candidate'),
                'start_time': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATETIME,
                    description='Start time in ISO 8601 format (e.g., 2023-11-01T12:00:00Z)'
                ),
                'end_time': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATETIME,
                    description='End time in ISO 8601 format (e.g., 2023-11-01T12:00:00Z)'
                ),
                'mandat_data': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATETIME,
                    description='Mandat time in ISO 8601 format (e.g., 2023-11-01T12:00:00Z)'
                ),
            },
            required=['name', 'duration', 'questions', 'limit for candidate', 'start_time', 'end_time', 'mandat_data']
        ),
        responses={200: DefaultSerializer()},
        tags=['quiz'],
    )
    def create_default_exam(self, request, *args, **kwargs):
        user = request.user
        request.data['user'] = user.id

        subject = Subject.objects.filter(id=request.data['subject']).first()

        if subject is None:
            return Response(data={'error': 'Subject not found'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DefaultSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Update Exam",
        operation_summary="Update Exam",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='test name'),
                'subject': openapi.Schema(type=openapi.TYPE_INTEGER, description='subject id'),
                'duration': openapi.Schema(type=openapi.TYPE_INTEGER, description='duration'),
                'questions': openapi.Schema(type=openapi.TYPE_INTEGER, description='questions'),
                'limit_for_candidates': openapi.Schema(type=openapi.TYPE_INTEGER, description='limit for candidate'),
                'start_time': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATETIME,
                    description='Start time in ISO 8601 format (e.g., 2023-11-01T12:00:00Z)'
                ),
                'end_time': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATETIME,
                    description='End time in ISO 8601 format (e.g., 2023-11-01T12:00:00Z)'
                ),
                'mandat_data': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATETIME,
                    description='Mandat time in ISO 8601 format (e.g., 2023-11-01T12:00:00Z)'
                ),
            },
            required=[]
        ),
        responses={200: DefaultSerializer()},
        tags=['quiz'],
    )
    def update_default_exam(self, request, *args, **kwargs):
        user = request.user
        request.data['user'] = user.id
        default_exam = DefaultExam.objects.filter(id=kwargs['pk']).first()

        if default_exam is None:
            return Response(data={'error': 'Default exam not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DefaultSerializer(default_exam, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if default_exam.user != request.user:
            return Response(data={'error': 'You have no permission to update this default exam'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(data={'result': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="delete exam",
        operation_description="delete exam",
        responses={200: 'Successfully deleted'},
        tags=['quiz'],
    )
    def delete_default_exam(self, request, *args, **kwargs):
        user = request.user
        default_exam = DefaultExam.objects.filter(id=kwargs['pk']).first()

        if default_exam is None:
            return Response(data={'error': 'Default exam not found'}, status=status.HTTP_404_NOT_FOUND)

        if user != default_exam.user:
            return Response(data={'error': 'You have no permission to delete this default exam'},
                            status=status.HTTP_400_BAD_REQUEST)

        default_exam.delete()

        return Response(data={'message': 'Default exam successfully deleted'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create Question",
        operation_summary="Create Question",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'subject': openapi.Schema(type=openapi.TYPE_INTEGER, description='subject'),
                'variant': openapi.Schema(type=openapi.TYPE_INTEGER, description='variant'),
                'question': openapi.Schema(type=openapi.TYPE_STRING, description='question'),
                'question_type': openapi.Schema(type=openapi.TYPE_INTEGER, description='question_type'),
                'A': openapi.Schema(type=openapi.TYPE_INTEGER, description='A'),
                'B': openapi.Schema(type=openapi.TYPE_INTEGER, description='B'),
                'C': openapi.Schema(type=openapi.TYPE_INTEGER, description='C'),
                'D': openapi.Schema(type=openapi.TYPE_INTEGER, description='D'),
                'correct_answer': openapi.Schema(type=openapi.TYPE_INTEGER, description='correct_answer'),
                'open_question_answer': openapi.Schema(type=openapi.TYPE_STRING, description='open_question_answer'),
            },
            required=['subject', 'variant', 'question', 'question_type']
        ),
        responses={200: CreateQuestionSerializer()},
        tags=['quiz'],
    )
    def create_question(self, request, *args, **kwargs):
        user = request.user
        request.data['user'] = user.id

        serializer = CreateQuestionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Update Question",
        operation_summary="Update Question",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'subject': openapi.Schema(type=openapi.TYPE_INTEGER, description='subject'),
                'variant': openapi.Schema(type=openapi.TYPE_INTEGER, description='variant'),
                'question': openapi.Schema(type=openapi.TYPE_INTEGER, description='question'),
                'question_type': openapi.Schema(type=openapi.TYPE_INTEGER, description='question_type'),
                'A': openapi.Schema(type=openapi.TYPE_INTEGER, description='A'),
                'B': openapi.Schema(type=openapi.TYPE_INTEGER, description='B'),
                'C': openapi.Schema(type=openapi.TYPE_INTEGER, description='C'),
                'D': openapi.Schema(type=openapi.TYPE_INTEGER, description='D'),
                'correct_answer': openapi.Schema(type=openapi.TYPE_INTEGER, description='correct_answer'),
                'open_question_answer': openapi.Schema(type=openapi.TYPE_STRING, description='open_question_answer'),
            },
            required=[]
        ),
        responses={200: CreateQuestionSerializer()},
        tags=['quiz'],
    )
    def update_question(self, request, *args, **kwargs):
        user = request.user
        request.data['user'] = user.id
        question = Question.objects.filter(id=kwargs['pk']).first()

        if question is None:
            return Response(data={'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CreateQuestionSerializer(question, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if question.user != user:
            return Response(data={'error': 'You have no permission to update this question'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(data={'result': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Delete Question",
        operation_description="Delete Question",
        responses={200: 'Successfully deleted'},
        tags=['quiz'],
    )
    def delete_question(self, request, *args, **kwargs):
        user = request.user
        question = Question.objects.filter(id=kwargs['pk']).first()

        if question is None:
            return Response(data={'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

        if user != question.user:
            return Response(data={'error': 'You have no permission to delete this question'},
                            status=status.HTTP_400_BAD_REQUEST)

        question.delete()

        return Response(data={'message': 'Question successfully deleted'}, status=status.HTTP_200_OK)

