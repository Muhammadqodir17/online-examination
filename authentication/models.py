from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLE = (
    (1, 'Candidate'),
    (2, 'Teacher'),
)


class User(AbstractUser):
    role = models.IntegerField(choices=USER_ROLE, default=1)

    def __str__(self):
        return f'{self.username}'
