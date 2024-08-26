from rest_framework import generics
from .models import Post
from .serializers import PostSerializer
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
    serializer_class = PostSerializer

