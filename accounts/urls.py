from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'accounts'

urlpatterns=[
    # AUTH URLS:
    path('users/signup', views.SignUpView.as_view(), name='signup'),
    path('users/login', views.LoginView.as_view(), name='login'),
    path('users/login/refresh', TokenRefreshView.as_view(), name='login_refresh'),
    path('users/logout', views.LogoutView.as_view(), name='logout'),
]

