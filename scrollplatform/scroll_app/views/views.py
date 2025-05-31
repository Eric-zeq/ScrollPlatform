from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from ..forms.user import LoginForm, RegisterForm, UserEditForm
from ..forms.post import PostForm
from ..models.models import Post, CustomUser, PostImage

# Create your views here.
def home(request):
     # 使用 prefetch_related 预取 Post 关联的 PostImage
    posts = Post.objects.prefetch_related('images').all().order_by('-created_at')
    return render(request,'base.html',{'posts':posts})

def navbar(request):
    return render(request,'nav.html')


def sendPost(request):
    return render(request,'sendPost.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # 登录成功后跳转到个人资料页面
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            user = form.save()
            login(request, user)  # 注册成功后自动登录
            return redirect('home')  # 跳转到个人资料页面
        else:
            # 打印或返回表单错误信息
            print(form.errors)
            return render(request, 'login.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('home')

def profile_edit_view(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST,request.FILES,instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('profile')  # 重定向到用户个人主页或其他页面
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'user_form': user_form,
    }
    return render(request, 'profile_edit.html', context)

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

            return redirect('home')  # 重定向到首页
    else:
        post_form = PostForm()
    return render(request,'sendPost.html', {'post_form': post_form})



def post_detail_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_detail.html', {'post': post})