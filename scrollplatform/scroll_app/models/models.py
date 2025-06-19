from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from .extra import user_directory_path



# Create your models here.

#user model
class CustomUser(AbstractUser):
    user_id = models.AutoField(primary_key=True)  # UserID
    email = models.EmailField(unique=True)       # Email
    avatar = models.ImageField(upload_to='avatars/', blank=True,null=True, default='avatars/user.png')  # avatar
    bio = models.TextField(blank=True, null=True)  # user bio
    USERNAME_FIELD = 'email'  # use email as username
    REQUIRED_FIELDS = ['username']  # require username field

      # rewrote groups and user_permissions fields to add related_name
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',  # define related_name for groups
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',  # define related_name for user_permissions
        related_query_name='customuser',
    )

    def __str__(self):
        return self.email
    

#Post model
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)  # Post ID
    title = models.CharField(max_length=100)  # title
    content = models.TextField()  # content
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')  # author
    is_public = models.BooleanField(default=True)  # is public
    is_commentable = models.BooleanField(default=True)  # is commentable
    created_at = models.DateTimeField(auto_now_add=True)  # created time
    updated_at = models.DateTimeField(auto_now=True)  # updated time

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
    

#Comment model
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)  # Comment ID
    content = models.TextField()  # comment content
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')  # comment author
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # post commented
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, 
                                       related_name='children_comments', null=True, blank=True)  # parent comment
    created_at = models.DateTimeField(auto_now_add=True)  # created time
    updated_at = models.DateTimeField(auto_now=True)  # updated time

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


#Like model
class LikesPost(models.Model):
    like_id = models.AutoField(primary_key=True)  # Like ID
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes_post')  # user
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes_post')  # post liked
    created_at = models.DateTimeField(auto_now_add=True)  # created time
    updated_at = models.DateTimeField(auto_now=True)  # updated time

    def __str__(self):
        return f"Like by {self.user.username} on {self.post.title}"


#Collect model
class CollectPost(models.Model):
    collect_id = models.AutoField(primary_key=True)  # Collect ID
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='collect_post')  # user
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='collect_post')  # post collected
    created_at = models.DateTimeField(auto_now_add=True)  # created time
    updated_at = models.DateTimeField(auto_now=True)  # updated time

    def __str__(self):
        return f"Collect by {self.user.username} on {self.post.title}"

#follow model
class flowsUser(models.Model):
    follow_id = models.AutoField(primary_key=True)  # Follow ID
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower')  # follower
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')  # following
    created_at = models.DateTimeField(auto_now_add=True)  # created time
    updated_at = models.DateTimeField(auto_now=True)  # updated time

    def __str__(self):
        return f"Follow by {self.follower.username} on {self.following.username}"

