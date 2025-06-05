from django.urls import path
from .views import views  
urlpatterns = [
    path('', views.home, name='home'),
    path('sendPost',views.sendPost,name='sendPost'),
    path('login/', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('profile', views.profile_view, name='profile'),
    path('logout', views.logout_view, name='logout'),
    path('profile_edit', views.profile_edit_view, name='profile_edit'),
    path('sendPost_view', views.sendPost_view, name='sendPost_view'),
    # path('post_list', views.post_list_view, name='post_list'),
    path('submit_comment', views.submit_comment, name='submit_comment'),
    path('post_detail/<int:post_id>', views.post_detail_view, name='post_detail'),
    path('add_like', views.toggle_like, name='like_post'),
    path('add_collect', views.toggle_collect, name='collect_post'),
    path('add_follow', views.toggle_follow, name='follow_user')

    
]