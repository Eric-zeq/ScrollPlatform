from rest_framework import viewsets
from ..serializers import UserSerializer,PostSerializer,CommentSerializer
from ..models import CustomUser,Post,Comment

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Post.objects.filter(is_public=True)
        else:
            return Post.objects.filter(author=user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Comment.objects.filter(post__is_public=True)
        else:
            return Comment.objects.filter(author=user)  