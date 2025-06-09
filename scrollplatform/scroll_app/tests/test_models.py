from django.test import TestCase
from ..models import Post, Comment,CustomUser

#test for CustomUser model
class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser', email='test@test.com', password='password')

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, CustomUser))

#test for Post model
class PostModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser', email='test@test.com', password='password')
        self.post = Post.objects.create(title='test title', content='test content', author=self.user)

    def test_post_creation(self):
        self.assertTrue(isinstance(self.post, Post))
        self.assertEqual(self.post.__str__(), 'test title')

#test for Comment model
class CommentModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser', email='test@test.com', password='password')
        self.post = Post.objects.create(title='test title', content='test content', author=self.user)
        self.comment = Comment.objects.create(content='test comment', author=self.user, post=self.post)

    def test_comment_creation(self):
        self.assertTrue(isinstance(self.comment, Comment))
        self.assertEqual(self.comment.__str__(), 'Comment by testuser on test title')

