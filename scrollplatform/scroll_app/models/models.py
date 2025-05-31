from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from .extra import user_directory_path



# Create your models here.

#user model
class CustomUser(AbstractUser):
    user_id = models.AutoField(primary_key=True)  # 用户ID
    email = models.EmailField(unique=True)       # 邮箱（唯一）
    avatar = models.ImageField(upload_to='avatars/', blank=True,null=True, default='avatars/user.png')  # 头像
    bio = models.TextField(blank=True, null=True)  # 个人说明
    USERNAME_FIELD = 'email'  # 使用邮箱作为登录字段
    REQUIRED_FIELDS = ['username']  # 必填字段

      # 重写 groups 和 user_permissions 字段，添加 related_name
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',  # 自定义反向关联名称
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',  # 自定义反向关联名称
        related_query_name='customuser',
    )

    def __str__(self):
        return self.email
    

#Post model
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)  # 文章ID
    title = models.CharField(max_length=100)  # 标题
    content = models.TextField()  # 内容
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')  # 作者
    # location = models.CharField(max_length=100, blank=True, null=True)  # 位置
    is_public = models.BooleanField(default=True)  # 是否公开
    is_commentable = models.BooleanField(default=True)  # 是否可评论
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_at = models.DateTimeField(auto_now=True)  # 更新时间

    def __str__(self):
        return self.title
    




#PostImage model
class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=user_directory_path, 
        blank=True, 
        null=True)

    def __str__(self):
        return f"Image for {self.post.title}"
