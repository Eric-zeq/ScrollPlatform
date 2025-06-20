from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from ..models import Post,Comment

class TestViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # create a user and login
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@test.com',
            password='password'
        )
        self.client.force_login(self.user)  # simulate login

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
        # use redirect('home')， 302
        self.assertEqual(response.status_code, 302)
        
        # if not redirect, it means the post is created successfully
        self.assertTrue(Post.objects.filter(title='test title').exists())
    
    def test_post_detail(self):
        # create a post
        url = reverse('post_detail', args=[self.post.post_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test title')
        self.assertContains(response, 'test content')

    def test_submit_comment_successfully(self):
        url = reverse('submit_comment')  # make sure name='submit_comment' in urls.py
        data = {
            'content': 'This is a test comment.',
            'post_id': self.post.post_id,
        }
        response = self.client.post(url, data)
        # should redirect to post_detail page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post_detail', args=[self.post.post_id]))
        # check if the comment is created
        self.assertTrue(Comment.objects.filter(content='This is a test comment.').exists())


