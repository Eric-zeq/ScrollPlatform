from rest_framework import serializers
from .models.models import CustomUser,Post,Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'username', 'email', 'avatar', 'bio', 'groups', 'user_permissions']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['post_id', 'title', 'content', 'author', 'is_public', 'is_commentable', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment_id', 'content', 'author', 'post', 'parent_comment', 'created_at', 'updated_at']