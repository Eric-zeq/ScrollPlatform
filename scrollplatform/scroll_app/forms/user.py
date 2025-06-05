from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from ..models.models import CustomUser

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")  # 替换默认的用户名为邮箱


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2', 'avatar', 'bio')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar', 'bio']  # 允许编辑的字段