from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from ..models import Post,Comment

# class TestViews(TestCase):
#     def setUp(self):
#         self.client = APIClient()
        
#         # 创建用户用于测试
#         self.user = get_user_model().objects.create_user(
#             username='testuser',
#             email='test@test.com',
#             password='password'
#         )
#         self.client.force_login(self.user)  # 模拟登录

#         self.post = Post.objects.create(
#             title='test title',
#             content='test content',
#             author=self.user
#         )

#     def test_send_post(self):
#         url = reverse('sendPost_view')
#         data = {
#             'title': 'test title',
#             'content': 'test content'
#         }
#         response = self.client.post(url, data)
#         # 因为你用了 redirect('home')，状态码会是 302
#         self.assertEqual(response.status_code, 302)
#         # 可选：断言是否创建了 Post

#         self.assertTrue(Post.objects.filter(title='test title').exists())
    
#     def test_post_detail(self):
#         # 创建一个 Post
#         url = reverse('post_detail', args=[self.post.post_id])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'test title')
#         self.assertContains(response, 'test content')

#     def test_submit_comment_successfully(self):
#         url = reverse('submit_comment')  # 确保 urls.py 中设置了 name='submit_comment'
#         data = {
#             'content': 'This is a test comment.',
#             'post_id': self.post.post_id,
#         }
#         response = self.client.post(url, data)
#         # 应该重定向到 post_detail 页面
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse('post_detail', args=[self.post.post_id]))
#         # 检查是否创建了评论
#         self.assertTrue(Comment.objects.filter(content='This is a test comment.').exists())



from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import tempfile
import os
from ..models import CustomUser  # 替换为你的 User 模型
@override_settings(MEDIA_ROOT=tempfile.mkdtemp())  # 临时目录用于测试文件上传
class ProfileEditViewTest(TestCase):
    def setUp(self):
        # 创建测试用户
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.client.login(username='test@example.com', password='password123')
        # 创建一个内存中的小图像用于上传测试
        image = Image.new('RGB', (100, 100))
        image_path = os.path.join(tempfile.gettempdir(), 'test_image.jpg')
        image.save(image_path)
        with open(image_path, 'rb') as img:
            self.uploaded_file = SimpleUploadedFile(
                name='test_avatar.jpg',
                content=img.read(),
                content_type='image/jpeg'
            )
    def test_profile_edit_get(self):
        """测试 GET 请求是否能正常打开页面"""
        response = self.client.get(reverse('profile_edit'))  # 确保你设置了 url 名为 profile_edit
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_edit.html')
    def test_profile_edit_post_valid(self):
        """测试有效的 POST 请求，包含头像上传"""
        post_data = {
            'username': 'new_username',
            'bio': 'This is a new bio.',
            'avatar': self.uploaded_file,
        }
        response = self.client.post(reverse('profile_edit'), post_data)
        
        # 刷新用户对象以获取最新数据
        self.user.refresh_from_db()
        # 检查是否重定向
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        # 检查字段是否更新成功
        self.assertEqual(self.user.username, 'new_username')
        self.assertEqual(self.user.bio, 'This is a new bio.')
        self.assertIn('test_avatar.jpg', self.user.avatar.name)
    def test_profile_edit_post_invalid(self):
        """测试无效的 POST 请求（比如不合法的文件格式）"""
        post_data = {
            'username': '',
            'bio': '',
            'avatar': self.uploaded_file,
        }
        response = self.client.post(reverse('profile_edit'), post_data)
        # 因为 username 是必填字段，所以表单应该出错
        self.assertEqual(response.status_code, 200)
        form = response.context['user_form']
        self.assertTrue(form.errors)
        self.assertIn('username', form.errors)
    def tearDown(self):
        # 清理测试文件
        if hasattr(self.user, 'avatar') and self.user.avatar:
            self.user.avatar.delete()

