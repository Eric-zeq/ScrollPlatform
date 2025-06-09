from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from ..models.models import CustomUser
from django.core.exceptions import ValidationError

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")  # 替换默认的用户名为邮箱


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2', 'avatar', 'bio')

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email has been registered!")
        return email

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'avatar', 'bio']  # 允许编辑的字段
    