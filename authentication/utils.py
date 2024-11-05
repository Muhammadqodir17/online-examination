import random
from rest_framework.response import Response
from rest_framework import status


def generate_otp():
    return random.randint(100000, 999999)


def register(password, confirm_password):
    if len(password) < 8:
        return Response(data={'error': 'Password must be at least 8 characters long'},
                        status=status.HTTP_400_BAD_REQUEST)

    forbidden_characters = set("!@#$%^&*/,.")
    if any(char in forbidden_characters for char in password):
        return Response(data={'error': 'Password cannot contain special characters: !@#$%^&*/,.'},
                        status=status.HTTP_400_BAD_REQUEST)

    if not any(char.isdigit() for char in password):
        return Response(data={'error': 'Password must contain at least one digit'},
                        status=status.HTTP_400_BAD_REQUEST)

    if not any(char.isalpha() for char in password):
        return Response(data={'error': 'Password must contain at least one letter'},
                        status=status.HTTP_400_BAD_REQUEST)

    if password != confirm_password:
        return Response(data={'error': 'Passwords do not match'},
                        status=status.HTTP_400_BAD_REQUEST)

    return password
