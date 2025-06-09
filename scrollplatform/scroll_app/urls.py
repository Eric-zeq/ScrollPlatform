from django.urls import path,include
from .views import views,view_api
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('api/v1/users', view_api.UserViewSet, basename='user')
router.register('api/v1/posts', view_api.PostViewSet, basename='post')
router.register('api/v1/comments', view_api.CommentViewSet, basename='comment')

urlpatterns = [
    path('', views.home, name='home'),
    path('sendPost',views.sendPost,name='sendPost'),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('forgot_password', views.forgot_password_view, name='forgot_password'),
    path('profile', views.profile_view, name='profile'),
    path('logout', views.logout_view, name='logout'),
    path('profile_edit', views.profile_edit_view, name='profile_edit'),
    path('sendPost_view', views.sendPost_view, name='sendPost_view'),
    path('submit_comment', views.submit_comment, name='submit_comment'),
    path('post_detail/<int:post_id>', views.post_detail_view, name='post_detail'),
    path('add_like', views.toggle_like, name='like_post'),
    path('add_collect', views.toggle_collect, name='collect_post'),
    path('add_follow', views.toggle_follow, name='follow_user'),
    path('notification', views.notification_view, name='notification'),
    path('search_view', views.search_view, name='search_view'),
    #Api
    path('api/v1/', include(router.urls)),
    
]