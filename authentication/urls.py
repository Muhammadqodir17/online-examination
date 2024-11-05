from django.urls import path
from .views import AuthViewSet


urlpatterns = [
    path('register/', AuthViewSet.as_view({'post': 'register'})),
    path('login/', AuthViewSet.as_view({'post': 'login'})),
    path('reset_password/', AuthViewSet.as_view({'post': 'reset_password'})),
]