from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, ProfileDetailView, ListFollowers, followed_accounts

#<app>/<model>_<viewtype>.html
#post/

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('new/', PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),

    path('search_user/', views.search_user, name='search-user'),
    path('like/', views.like_post, name='like-post'),

    #path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('profile/<int:pk>/followers/', ListFollowers.as_view(), name='profile-list'),
    path('followed/', views.followed_accounts, name='followed-acc'),
    path('about/', views.about, name='about')
    
    
]