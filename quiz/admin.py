from django.contrib import admin
from .models import (
    Subject,
    Question,
    Exam,
    DefaultExam,
    QuestionType,
    Result,
    Answer
)


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'subject', 'variant', 'question_type', ]
    list_display_links = ['id', 'user', 'subject', 'variant', 'question_type', ]
    search_fields = ['id', 'user__username']
    list_filter = ['subject', 'variant', 'question_type', ]


class AnswersAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'question', 'question_type', 'answer', 'true_or_false',
                    'status_for_checked_or_unchecked', ]

    list_display_links = ['id', 'user', 'question', 'question_type', 'answer', 'true_or_false',
                          'status_for_checked_or_unchecked', ]

    search_fields = ['id', 'user__username',
                     'true_or_false', ]

    list_filter = ['status_for_checked_or_unchecked', 'question_type']


class DefaultExamAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'duration', 'questions', 'limit_for_candidates',
                    'start_time', 'end_time', 'mandat_data']

    list_display_links = ['id', 'user', 'name', 'duration', 'questions', 'limit_for_candidates',
                          'start_time', 'end_time', 'mandat_data']


class ExamAdmin(admin.ModelAdmin):
    list_display = ['id', 'default', 'user', 'subject', 'variant', ]
    list_display_links = ['id', 'default', 'user', 'subject', 'variant', ]
    search_fields = ['id', 'default__name', 'user__username',]
    list_filter = ['subject', 'variant']


class ResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'exam', 'total_questions', 'correct_answers', 'status_for_checked_or_unchecked', ]
    list_display_links = ['id', 'exam', 'total_questions', 'correct_answers', 'status_for_checked_or_unchecked', ]
    search_fields = ['id', 'total_questions', 'correct_answers', ]
    list_filter = ['status_for_checked_or_unchecked', ]


class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    list_display_links = ['id', 'name', ]
    search_fields = ['id', 'name']
    list_filter = ['name', ]


admin.site.register(Subject)
admin.site.register(Question, QuestionsAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Answer, AnswersAdmin)
admin.site.register(DefaultExam, DefaultExamAdmin)
admin.site.register(QuestionType, QuestionTypeAdmin)
