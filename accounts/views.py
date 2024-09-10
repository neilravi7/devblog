# django core imports
from django.contrib.auth import get_user_model

# rest_framework imports
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

# Token Views (Authentication)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken

# serializers imports
from . import serializers
from .models import Followers


# Auth API's
class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer


class LoginView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer
    


# Players API's
class UserList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer
    queryset = get_user_model().objects.all()


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer
    queryset = get_user_model().objects.all()
    lookup_field = 'pk'

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserProfileSerializer
    queryset = get_user_model().objects.all()
    lookup_field = 'pk'

class UserDelete(generics.DestroyAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer
    lookup_field = 'pk'


class UserPartialUpdate(generics.UpdateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UpdateUserSerializer
    queryset = get_user_model().objects.all()
    lookup_field = 'pk'


# class ChangePasswordView(generics.UpdateAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = serializers.ChangePasswordSerializer
#     queryset = get_user_model().objects.all()
#     lookup_field = 'pk'

 
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            print(token)
            token.blacklist()
            return Response({"message":"user logout"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"message":str(e)} , status=status.HTTP_400_BAD_REQUEST)
        

class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


class FollowUserView(generics.CreateAPIView):
    """API for following a user"""
    permission_classes = [IsAuthenticated]
    queryset = Followers.objects.all()
    serializer_class = serializers.FollowerSerializer

    def perform_create(self, serializer):
        user_to_follow_id = self.request.data.get('user')  # ID of the user to follow
        follower = self.request.user

        if follower.id == user_to_follow_id:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if Followers.objects.filter(user_id=user_to_follow_id, follower=follower).exists():
            return Response({"error": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user_id=user_to_follow_id, follower=follower)


class UnfollowUserView(generics.DestroyAPIView):
    """API for unfollowing a user"""
    permission_classes = [IsAuthenticated]
    queryset = Followers.objects.all()
    lookup_field = 'user'  # The ID of the user to unfollow

    def delete(self, request, *args, **kwargs):
        user_to_unfollow_id = kwargs['user']
        follower = self.request.user

        # Check if the follower relationship exists
        try:
            follow_instance = Followers.objects.get(user_id=user_to_unfollow_id, follower=follower)
            follow_instance.delete()
            return Response({"message": "Successfully unfollowed the user."}, status=status.HTTP_204_NO_CONTENT)
        except Followers.DoesNotExist:
            return Response({"error": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)
