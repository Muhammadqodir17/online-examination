from django.urls import path
from .views import SubjectViewSet

urlpatterns = [
    path('subjects/', SubjectViewSet.as_view({'get': 'get_all'}), name='subjects'),
    path('choose_subjects/<int:pk>/', SubjectViewSet.as_view({'get': 'choose_subjects'}), name='choose_subjects'),
    path('start/<int:pk>/', SubjectViewSet.as_view({'get': 'start_test'}), name='start'),
    path('answer/<int:pk>/', SubjectViewSet.as_view({'post': 'answer'}), name='answer'),
    path('mandat/', SubjectViewSet.as_view({'post': 'mandat'}), name='mandat'),
    # exam
    path('create_default_exam/', SubjectViewSet.as_view({'post': 'create_default_exam'}), name='create_default_exam'),
    path('update_default_exam/<int:pk>/', SubjectViewSet.as_view({'patch': 'update_default_exam'}),
         name='update_default_exam'),
    path('delete_default_exam/<int:pk>/', SubjectViewSet.as_view({'delete': 'delete_default_exam'}),
         name='delete_default_exam'),
    # question
    path('create_question/', SubjectViewSet.as_view({'post': 'create_question'}), name='create_question'),
    path('update_question/<int:pk>/', SubjectViewSet.as_view({'patch': 'update_question'}), name='update_question'),
    path('delete_question/<int:pk>/', SubjectViewSet.as_view({'delete': 'delete_question'}), name='delete_question'),
    # # subject
    # path('create_subject/', SubjectViewSet.as_view({'post': 'create_subject'})),
    # path('update_subject/<int:pk>/', SubjectViewSet.as_view({'patch': 'update_subject'})),
    # path('delete_subject/<int:pk>/', SubjectViewSet.as_view({'delete': 'delete_subject'})),
]
