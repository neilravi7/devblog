from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'slug', 'content', 'author', 'postImage']
        # read_only_fields = ('id', 'slug', 'author', 'postImage')

    def create(self, validated_data):
        # Create a new Post instance with the validated data
        print("validated_data:", validated_data)
        post = Post.objects.create(**validated_data)
        return post
