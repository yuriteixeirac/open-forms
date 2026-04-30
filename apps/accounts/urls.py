from django.urls import path
from apps.accounts.views import register_view, login_view


urlpatterns = [
    path('register/', register_view, name='register-view'),
    path('login/', login_view, name='login-view'),
]
