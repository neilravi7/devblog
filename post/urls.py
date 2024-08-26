from django.urls import path
from .views import PostCreateView, PostView, PublicPostListView

urlpatterns = [
    path('posts', PublicPostListView.as_view(), name='post-list'),
    path('post/create', PostCreateView.as_view(), name='post-create'),
    path('post/<uuid:pk>', PostView.as_view(), name='post-view'),
]
