from django import forms
from ..models.models import Post, Comment

# class MultipleFileInput(forms.ClearableFileInput):
#     allow_multiple_selected = True  # 关键属性

# class MultipleFileField(forms.FileField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault("widget", MultipleFileInput())
#         super().__init__(*args, **kwargs)

#     def clean(self, data, initial=None):
#         if isinstance(data, (list, tuple)):
#             return [super().clean(d, initial) for d in data]
#         return super().clean(data, initial)

# class MultipleFileForm(forms.Form):
#     forms.ClearableFileInput.allow_multiple_selected = True # 关键属性
#     files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
   

class PostForm(forms.ModelForm):
   forms.ClearableFileInput.allow_multiple_selected = True # keyword attribute
   images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                            required=False,  # allow empty images
                            label="Upload multiple images"
                            )
   
   class Meta:
        model = Post
        fields = ['title', 'content', 'is_public', 'is_commentable']
        



