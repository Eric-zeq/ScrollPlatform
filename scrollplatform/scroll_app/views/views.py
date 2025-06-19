from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from ..forms.user import LoginForm, RegisterForm, UserEditForm
from ..forms.post import PostForm
from ..models.models import Post, PostImage,Comment,LikesPost,CollectPost,CustomUser,flowsUser
from itertools import chain
from django.db.models import Value
from django.db.models.fields import CharField 
from django.contrib import messages
import datetime
import logging

logger = logging.getLogger(__name__)


# Create your views here.
def home(request):
    logger.info('Homepage was accessed at '+str(datetime.datetime.now())+' hours!')
     # 使用 prefetch_related 预取 Post 关联的 PostImage
    posts = Post.objects.filter(is_public=True).prefetch_related('images').all().order_by('-created_at')
    return render(request,'base.html',{'posts':posts})

def navbar(request):
    return render(request,'nav.html')


def sendPost(request):
    return render(request,'sendPost.html')

#login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # After login, redirect to home page
            else:
                logger.error('Login failed for user '+email+' at '+str(datetime.datetime.now())+' hours!')
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

#register view
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        print(form.errors)
        print(form.data)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after registration
            return redirect('home')  # After registration, redirect to home page
        else:
            return render(request, 'login.html', {'form': form,'show_signup': True,})
    else:
        form = RegisterForm()
    return render(request, 'login.html', {'form': form,'show_signup': True})

#logout view
def logout_view(request):
    logout(request)
    return redirect('home')

#forgot password view
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('password1')
        try:
            user = CustomUser.objects.get(email=email)
            # if password is not set, set it to the new password
            if not new_password:
                messages.error(request, "Please enter a new password.")
                return render(request, 'login.html', {'show_forget': True, 'email': email})
            # set the new password
            user.set_password(new_password)
            user.save()
            return redirect('login')  # redirect to login page
        except CustomUser.DoesNotExist:
            messages.error(request, "Email does not exist.")
            return render(request, 'login.html', {'show_forget': True, 'email': email})
    return render(request, 'login.html', {'show_forget': True})

#profile view
@login_required
def profile_view(request):
    follows = flowsUser.objects.filter(follower=request.user).count()
    followed = flowsUser.objects.filter(following=request.user).count()
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    post_likes = LikesPost.objects.filter(user=request.user).order_by('-created_at')
    post_collects = CollectPost.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'user': request.user, 
                                            'follows': follows, 'followed': followed,
                                             'posts': posts, 
                                             'post_likes': post_likes, 'post_collects': post_collects})

#profile edit view
@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        data = request.POST
        files = request.FILES
        user_form = UserEditForm(data,files,instance=request.user)
        print(user_form.data)
        if user_form.is_valid():
            user_form.save()
            return redirect('profile')  # redirect to profile page
        else:
            print(user_form.errors)  # 👈 加上这一行看具体出错的地方
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'user_form': user_form,
    }
    return render(request, 'profile_edit.html', context)


#send post view
def sendPost_view(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        print(post_form.errors)
        print(post_form.data)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            images = request.FILES.getlist('post_images')
            for image in images:
                PostImage.objects.create(post=post, image=image)
            logger.info('Post '+str(post.post_id)+' was created at '+str(datetime.datetime.now())+' hours!')
            return redirect('home') 
    else:
        post_form = PostForm()
    return render(request,'sendPost.html', {'post_form': post_form})


#post detail view
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post,parent_comment=None).prefetch_related('children_comments','author').order_by('created_at')
    likes = LikesPost.objects.filter(post=post)
    collects = CollectPost.objects.filter(post=post)
    is_liked = False
    is_collected = False
    is_followed = False
    # only user logged in can like or collect or follow
    if request.user.is_authenticated:
        is_liked = LikesPost.objects.filter(post=post, user=request.user).exists()
        is_collected = CollectPost.objects.filter(post=post, user=request.user).exists()
        is_followed = flowsUser.objects.filter(follower=request.user, following=post.author).exists()
    
    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'likes': likes,
        'collects': collects,
        'is_liked': is_liked,
        'is_collected': is_collected,
        'is_followed': is_followed,
    })

#comment view
def submit_comment(request):
    if request.method == 'POST':
        print(request.POST)
        content = request.POST.get('content')
        post_id = request.POST.get('post_id')
        parent_id = request.POST.get('parent_id', None)
        post = get_object_or_404(Post, pk=post_id)
        parent_comment = get_object_or_404(Comment, pk=parent_id) if parent_id else None
        comment = Comment.objects.create(
            content=content,
            author=request.user,
            post=post,
            parent_comment=parent_comment
        )
        print(comment)
        return redirect('post_detail', post_id=post_id)
    else:
        return redirect('home')


#like post view
def toggle_like(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        user = request.user
        like_post, created = LikesPost.objects.get_or_create(post=post, user=user)

        if created:
            like_post.save()
        else:
            like_post.delete()
        
        return redirect('post_detail', post_id=post_id)
    else:
        return redirect('home')

#collect post view
def toggle_collect(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        user = request.user
        collect_post, created = CollectPost.objects.get_or_create(post=post, user=user)
        if created:
            collect_post.save()
        else:
            collect_post.delete()
        return redirect('post_detail', post_id=post_id)
    else:
        return redirect('home')

#follow user view
def toggle_follow(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        post_id = request.POST.get('post_id')
        user = get_object_or_404(CustomUser, pk=user_id)
        follow_user, created = flowsUser.objects.get_or_create(follower=request.user, following=user)
        if created:
            follow_user.save()
        else:
            follow_user.delete()
        return redirect('post_detail', post_id=post_id)
    else:
        return redirect('home')

#notification view
def notification_view(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    comments = Comment.objects.filter(post__in=user_posts).order_by('-created_at')
    # get all posts, comments, likes, collects
    likes = LikesPost.objects.filter(post__in=user_posts).annotate(action_type=Value('like', output_field=CharField()))
    collects = CollectPost.objects.filter(post__in=user_posts).annotate(action_type=Value('collect', output_field=CharField()))
    # combine likes and collects
    combined = sorted(
        chain(likes, collects),
        key=lambda x: x.created_at,
        reverse=True
    )
    follows = flowsUser.objects.filter(following=request.user).order_by('-created_at')
    print(follows)
    return render(request, 'notification.html', {'comments': comments, 'combined': combined, 'follows': follows})

#search view
def search_view(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        posts = Post.objects.filter(title__icontains=keyword)
        return render(request,'base.html', {'posts': posts, 'keyword': keyword})
    else:
        return redirect('home')