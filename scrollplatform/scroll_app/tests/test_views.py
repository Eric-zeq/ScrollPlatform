from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import tempfile
import os
from ..models import CustomUser  # 
@override_settings(MEDIA_ROOT=tempfile.mkdtemp())  # override the MEDIA_ROOT setting to a temporary directory for testing
class ProfileEditViewTest(TestCase):
    def setUp(self):
        # create a user for testing
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.client.login(username='test@example.com', password='password123')
        # create a memory-based small image for upload testing
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
        """Test if the profile edit page can be opened successfully"""
        response = self.client.get(reverse('profile_edit'))  # make sure you set the url name to 'profile_edit'
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_edit.html')
    def test_profile_edit_post_valid(self):
        """Test a valid POST request, including avatar upload"""
        post_data = {
            'username': 'new_username',
            'bio': 'This is a new bio.',
            'avatar': self.uploaded_file,
        }
        response = self.client.post(reverse('profile_edit'), post_data)
        
        # refresh the user object to get the latest data
        self.user.refresh_from_db()
        # check if the response is a redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        # check if the fields are updated successfully
        self.assertEqual(self.user.username, 'new_username')
        self.assertEqual(self.user.bio, 'This is a new bio.')
        self.assertIn('test_avatar.jpg', self.user.avatar.name)
    def test_profile_edit_post_invalid(self):
        """Test an invalid POST request (e.g. an invalid file format)"""
        post_data = {
            'username': '',
            'bio': '',
            'avatar': self.uploaded_file,
        }
        response = self.client.post(reverse('profile_edit'), post_data)
        # because 'username' is a required field, the form should fail
        self.assertEqual(response.status_code, 200)
        form = response.context['user_form']
        self.assertTrue(form.errors)
        self.assertIn('username', form.errors)
    def tearDown(self):
        # clean up the test file
        if hasattr(self.user, 'avatar') and self.user.avatar:
            self.user.avatar.delete()

