from django.urls import path
from . import views

urlpatterns = [
    # Post API's
    path('posts', views.PublicPostListView.as_view(), name='post-list'),
    path('post/create', views.PostCreateView.as_view(), name='post-create'),
    path('post/<uuid:pk>', views.PostView.as_view(), name='post-view'),
    path('post/<uuid:pk>/view', views.PostDetailView.as_view(), name='post-detail'),

    

    path('posts/<uuid:post_id>/comments', views.CommentCreateView.as_view(), name='comment-create'),
    path('posts/comments/<uuid:pk>', views.CommentRemoveView.as_view(), name='comment-remove'),
    path('posts/<uuid:post_id>/likes', views.LikeCreateView.as_view(), name='like-create'),
    path('posts/likes/<uuid:pk>', views.LikeRemoveView.as_view(), name='like-remove'),
]
