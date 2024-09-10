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

    # User API's
    path('users/<uuid:pk>', views.UserPartialUpdate.as_view(), name="partial-update"),
    path('users/<uuid:pk>/profile', views.UserProfileView.as_view(), name="profile"),


    # Follower API's
    path('users/following', views.FollowUserView.as_view(), name="follow"),
    path('users/unfollowing/<uuid:user>', views.UnfollowUserView.as_view(), name="unfollow"),

]

