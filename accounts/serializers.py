from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Profile, Followers
from post.serializers import NestedPostSerializer
from post.models import Post
# from django.contrib.auth.password_validation import validate_password



class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = ['user']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["success"] = True
        return data

# All custom serializers for nesting data for user profile view

class CustomFollowerSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField()  # Display username or other details

    class Meta:
        model = Followers
        fields = ['follower']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_image']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'slug', 'postImage', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    # user_type = serializers.CharField(write_only=True)

    # group =serializers.CharField()

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('password not match')
        return super().validate(data)
    
    
    def create(self, validated_data):        
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']

        user = self.Meta.model.objects.create_user(**data)

        user.save()

        return user
    
    class Meta:
        model = get_user_model()

        fields= (
            'id', 'email', 'password1', 'password2', 'first_name',
            'last_name',
        )
        read_only_fields = ('id', 'password1', 'password2',)


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != 'id':
                token[key] = value
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['userDetails'] = self.user.get_profile()       
        data['success'] = True
        return data

class UpdateUserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(max_length=120)
    profile_image = serializers.URLField(max_length=300)
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'first_name', 'last_name', 'bio', 'profile_image']
        read_only_fields = ('id', 'email',)

    def update(self, instance, validated_data):
        # Exclude password fields from validated data
        validated_data.pop('password1', None)
        validated_data.pop('password2', None)

        instance.profile.bio = validated_data['bio']
        instance.profile.profile_image = validated_data['profile_image']

        instance.profile.save()        
        instance = super().update(instance, validated_data)
        return instance
    
    def to_representation(self, instance):
        # Get the default serialized data
        data = super().to_representation(instance)

        # List of Users whom followed by user.
        following = [
            {
                "id":following.user.id, 
                "name":f'{following.user.first_name} {following.user.last_name}'
            } for following in instance.following.all()
        ]
        
        # List of Users whom followed user.
        followers = [
            {
                "id":follower.user.id, 
                "name":f'{follower.user.first_name} {follower.user.last_name}'
            } for follower in instance.followers.all()
        ]

        extra_data = {
            "following":following,
            "followers":followers,
            "user_id":instance.id            
        }
        
        # Merge extra data into the serialized data
        data.update(extra_data)
        
        return data

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    peoples_you_follow = FollowerSerializer(source='followers', many=True, read_only=True)
    peoples_following_you = FollowerSerializer(source='following', many=True, read_only=True)
    user_posts = NestedPostSerializer(source='posts', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'profile', 'peoples_you_follow', 'peoples_following_you', 'user_posts']