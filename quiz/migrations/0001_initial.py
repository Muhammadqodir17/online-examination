# Generated by Django 5.1.1 on 2024-10-30 19:42

import django.db.models.deletion
import quiz.utils
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('duration', models.PositiveIntegerField(default=60)),
                ('questions', models.PositiveIntegerField(default=30)),
                ('limit_for_candidates', models.PositiveIntegerField(default=30)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('mandat_data', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.IntegerField(choices=[(1, 'Math'), (2, 'English'), (3, 'Physics')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('variant', models.PositiveIntegerField(choices=[(1, 'Birinchi variant'), (2, 'Ikkinchi variant'), (3, 'Uchinchi variant')], default=quiz.utils.random_variant)),
                ('default', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.defaultexam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.subject')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('variant', models.IntegerField(choices=[(1, 'Birinchi variant'), (2, 'Ikkinchi variant'), (3, 'Uchinchi variant')])),
                ('question', models.TextField()),
                ('A', models.CharField(blank=True, max_length=100)),
                ('B', models.CharField(blank=True, max_length=100)),
                ('C', models.CharField(blank=True, max_length=100)),
                ('D', models.CharField(blank=True, max_length=100)),
                ('correct_answer', models.IntegerField(blank=True, choices=[(1, 'A'), (2, 'B'), (3, 'C'), (3, 'D')], null=True)),
                ('open_question_answer', models.CharField(blank=True, max_length=200)),
                ('question_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.questiontype')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.subject')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('answer', models.CharField(max_length=200)),
                ('true_or_false', models.BooleanField(default=False)),
                ('status_for_checked_or_unchecked', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question')),
                ('question_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.questiontype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('total_questions', models.PositiveIntegerField(default=0)),
                ('correct_answers', models.PositiveIntegerField(default=0)),
                ('status_for_checked_or_unchecked', models.BooleanField(default=False)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.exam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
