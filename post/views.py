from rest_framework import generics
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, NestedPostSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class PostCreateView(generics.CreateAPIView):
    """ Handles listing all posts and creating a new post.
    """ 
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """Set the author to the authenticated user when creating a post."""
        serializer.save(author=self.request.user)

class PostView(generics.RetrieveUpdateDestroyAPIView):
    """ Handles retrieving, updating, and deleting a specific post.
    """
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_update(self, serializer):
        """Ensure that the author remains the authenticated user when updating a post."""
        serializer.save(author=self.request.user)


class PublicPostListView(generics.ListAPIView):
    """Handles listing all posts
    """
    permission_classes = [AllowAny]
    queryset = Post.objects.all()
    serializer_class = NestedPostSerializer


class CommentCreateView(generics.CreateAPIView):
    """ to comment to post.
    """ 
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['post_id'])
        serializer.save(user=self.request.user, post=post)


class CommentRemoveView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    

class LikeCreateView(generics.CreateAPIView):
    """to like a post"""
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['post_id'])
        serializer.save(user=self.request.user, post=post)


class LikeRemoveView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()
    serializer_class = LikeSerializer