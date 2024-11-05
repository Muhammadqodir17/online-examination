# total_question = 0
# total_question += 1
#
# if request.data['answer'] > 4:
#     return Response(
#         data={'error': 'You have to choose 1 to 4 and 1 for "A", 2 for "B", 3 for "C" and 4 for "D"'})
#
# question = Question.objects.filter(id=request.data['question_id']).first()
# exam = Exam.objects.filter(id=kwargs['pk']).first
# default = DefaultExam.objects.all().order_by('-created_at').first()
# end_time = datetime.now() + timedelta(minutes=default.duration)
# result = Result.objects.filter(user=user, exam_id=kwargs['pk'])
#
# if end_time == datetime.now():
#     return Response(data={
#         'message': 'Time is up, Your result will be send your telegram soon'
#     })
#
# if total_question == exam.default.questions:
#     return Response(data={
#         'message': 'The test end, Your result will be send your telegram soon'
#     })
#
# if question is None:
#     return Response(data={'message': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
#
# if question.correct_answer == request.data['answer']:
#     result.correct_answers += 1

################for subject #############33

# @swagger_auto_schema(
#     operation_description="Update Subject",
#     operation_summary="Update Subject",
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'name': openapi.Schema(type=openapi.TYPE_STRING, description='name'),
#         },
#         required=['name']
#     ),
#     responses={200: SubjectSerializer()},
#     tags=['quiz'],
# )
# def create_subject(self, request, *args, **kwargs):
#     user = request.user
#     request.data['user'] = user.id
#
#     if not user.is_authenticated:
#         return Response(data={'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
#
#     exist_user = User.objects.filter(username=user, role=2).first()
#
#     if exist_user is None:
#         return Response(data={'error': 'You have no permission to create subject. '
#                                        'To create subject your role must be teacher'},
#                         status=status.HTTP_400_BAD_REQUEST)
#
#     serializer = SubjectSerializer(data=request.data)
#
#     if not serializer.is_valid():
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     serializer.save()
#
#     return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#
# @swagger_auto_schema(
#     operation_description="Update Subject",
#     operation_summary="Update Subject",
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'subject': openapi.Schema(type=openapi.TYPE_STRING, description='subject'),
#         },
#         required=['subject']
#     ),
#     responses={200: SubjectSerializer()},
#     tags=['quiz'],
# )
# def update_subject(self, request, *args, **kwargs):
#     user = request.user
#     request.data['user'] = user.id
#     subject = Subject.objects.filter(id=kwargs['pk']).first()
#
#     if not user.is_authenticated:
#         return Response(data={'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
#
#     if subject is None:
#         return Response(data={'error': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     serializer = SubjectSerializer(subject, data=request.data, partial=True)
#
#     if not serializer.is_valid():
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if subject.user != request.user:
#         return Response(data={'error': 'You have no permission to update this subject'},
#                         status=status.HTTP_400_BAD_REQUEST)
#
#     serializer.save()
#     return Response(data={'result': serializer.data}, status=status.HTTP_200_OK)
#
# @swagger_auto_schema(
#     operation_summary="Delete Subject",
#     operation_description="Delete Subject",
#     responses={200: 'Successfully deleted'},
#     tags=['quiz'],
# )
# def delete_subject(self, request, *args, **kwargs):
#     user = request.user
#     subject = Subject.objects.filter(id=kwargs['pk']).first()
#
#     if not user.is_authenticated:
#         return Response(data={'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
#
#     if subject is None:
#         return Response(data={'error': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     if user != subject.user:
#         return Response(data={'error': 'You have no permission to delete this subject'},
#                         status=status.HTTP_400_BAD_REQUEST)
#
#     subject.delete()
#
#     return Response(data={'message': 'Subject successfully deleted'}, status=status.HTTP_200_OK)
#
#############answer ##########33
# question_type = QuestionType.objects.filter(id=request.data['question_type']).first()
# if question is None:
#     return Response(data={'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
#
# if question_type is None:
#     return Response(
#         data={'message': 'You have to pick only one and write correctly ( 1 for close/ 2 for open )'})


a = '/api/v1/quiz/choose_subjects/1/'
l = len(a)
index = a[(l - 2):-1]
print(index)
print(a[:-1])
