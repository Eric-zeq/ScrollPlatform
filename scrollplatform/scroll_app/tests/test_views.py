from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from ..models import Post,Comment

class TestViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # 创建用户用于测试
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@test.com',
            password='password'
        )
        self.client.force_login(self.user)  # 模拟登录

        self.post = Post.objects.create(
            title='test title',
            content='test content',
            author=self.user
        )

    def test_send_post(self):
        url = reverse('sendPost_view')
        data = {
            'title': 'test title',
            'content': 'test content'
        }
        response = self.client.post(url, data)
        # 因为你用了 redirect('home')，状态码会是 302
        self.assertEqual(response.status_code, 302)
        # 可选：断言是否创建了 Post

        self.assertTrue(Post.objects.filter(title='test title').exists())
    
    def test_post_detail(self):
        # 创建一个 Post
        url = reverse('post_detail', args=[self.post.post_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test title')
        self.assertContains(response, 'test content')

    def test_submit_comment_successfully(self):
        url = reverse('submit_comment')  # 确保 urls.py 中设置了 name='submit_comment'
        data = {
            'content': 'This is a test comment.',
            'post_id': self.post.post_id,
        }
        response = self.client.post(url, data)
        # 应该重定向到 post_detail 页面
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post_detail', args=[self.post.post_id]))
        # 检查是否创建了评论
        self.assertTrue(Comment.objects.filter(content='This is a test comment.').exists())




