from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, Comment, Like
from taggit.serializers import TagListSerializerField, TaggitSerializer
from taggit.models import Tag
from .models import Category, Like


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    category = serializers.UUIDField()
    tags = TagListSerializerField()


    class Meta:
        model = Post
        fields = [
            'id','title', 'slug', 'content', 'postImage', "category", "tags"
        ]

    def create(self, validated_data):
        # Create a new Post instance with the validated data
        category_uuid = validated_data.pop('category', None)
        tags = validated_data.pop('tags', [])
        # print("validated_data:", validated_data)
        post = Post.objects.create(**validated_data)

        if category_uuid:
            post.category= Category.objects.get(id=category_uuid)
            post.save()
        # if tags:
        #     post.tags.set(*tags)
        #     post.save()
        
        return post
    
    def update(self, instance, validated_data):

        category_id = self.initial_data.get('category')
        if category_id:
            category = Category.objects.get(id=category_id)
            instance.category = category
        
        # Update the remaining fields
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
    

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','content', 'user', 'post']
    

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post']


"""Post Custom serializers"""

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

class CustomCommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'post']

class CustomLikeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'post']

class NestedPostSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    comments = CustomCommentSerializer(many=True, read_only=True)
    likes = CustomLikeSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'slug', 'author', 'postImage', 'comments', 'likes', 'category', 'tags', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        liked_by = [like.user.id for like in Like.objects.filter(post=instance)]
        data["likedBy"] = liked_by
        return data