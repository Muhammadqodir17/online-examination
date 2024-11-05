import jwt
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class CheckAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        line = len(request.path)
        request_path = request.path
        index = request_path[(line - 2):-1]

        token = request.headers.get('Authorization')
        target_urls = [
            '/api/v1/auth/reset_password/',
            '/api/v1/quiz/choose_subjects/',
            '/api/v1/quiz/start/',
            '/api/v1/quiz/answer/',
            '/api/v1/quiz/mandat/',
            '/api/v1/quiz/create_default_exam/',
            '/api/v1/quiz/update_default_exam/',
            '/api/v1/quiz/delete_default_exam/',
            '/api/v1/quiz/create_question/',
            '/api/v1/quiz/update_question/',
            '/api/v1/quiz/delete_question/',
        ]
        if index.isdigit() and request.path[:-2] in target_urls:
            if token is None:
                return JsonResponse(data={'error': 'Not authenticated'}, status=401)

            if token.split()[0] != 'Bearer':
                return JsonResponse(data={'error': 'Bearer is missed'}, status=400)

        if request.path in target_urls:
            if token is None:
                return JsonResponse(data={'error': 'Not authenticated'}, status=401)

            if token.split()[0] != 'Bearer':
                return JsonResponse(data={'error': 'Bearer is missed'}, status=400)


class RolePermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        target_urls = [
            reverse('create_default_exam'),
            reverse('create_question'),
        ]
        if request.path in target_urls:
            token = request.headers.get('Authorization')
            payload = jwt.decode(token.split()[1], settings.SECRET_KEY, algorithms=['HS256'])
            role = payload.get('role')

            if role != 2:
                return JsonResponse(data={'error': 'Permission denied'}, status=403)
