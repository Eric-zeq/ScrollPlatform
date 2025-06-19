from rest_framework.test import APITestCase
from ..serializers import UserSerializer,PostSerializer,CommentSerializer
from ..models import CustomUser,Post,Comment


class TestSerializers(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'password'
        }

        # 创建 post 所需的 author 用户
        self.author1 = CustomUser.objects.create_user(
            username='testuser2',
            email='test2@test.com',
            password='password'
        )
        # 创建 comment 所需的 author 用户
        self.author2 = CustomUser.objects.create_user(
            username='testuser3',
            email='test3@test.com',
            password='password'
        )

        self.post1 = Post.objects.create(
            title='test title1',
            content='test content1',
            author=self.author1,
        )


        self.post_data = {
            'title': 'test title',
            'content': 'test content',
            'author': self.author1,
        }


        self.comment_data = {
            'content': 'test comment',
            'post': self.post1,
            'author': self.author2,
        }

        self.user = CustomUser.objects.create_user(**self.user_data)
        self.post = Post.objects.create(**self.post_data)
        self.comment = Comment.objects.create(**self.comment_data)

    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user)
        self.assertEqual(serializer.data['username'], 'testuser')
        self.assertEqual(serializer.data['email'], 'test@test.com')

    def test_post_serializer(self):
        serializer = PostSerializer(instance=self.post)
        self.assertEqual(serializer.data['title'], 'test title')
        self.assertEqual(serializer.data['content'], 'test content')
        self.assertEqual(serializer.data['author'], self.author1.user_id)


    def test_comment_serializer(self):
        serializer = CommentSerializer(instance=self.comment)
        self.assertEqual(serializer.data['content'], 'test comment')
        self.assertEqual(serializer.data['post'], self.post1.post_id)
        self.assertEqual(serializer.data['author'], self.author2.user_id)
