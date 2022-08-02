from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from . models import Post, Like
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import FollowersCount, Profile
from itertools import chain


def home(request):
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'post/home.html', context)

def about(request):
    return render(request, 'post/about.html')

class PostListView(ListView):
    model = Post
    template_name = 'post/home.html'
    context_object_name = 'posts'
    ordering = ['-date']

    paginate_by = 7


class UserPostListView(ListView):
    model = Post
    template_name = 'post/user_posts.html'
    context_object_name = 'posts'

    paginate_by = 7
    #limit post on page to an specific user
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    #setting the author of the post equal to the current logged in user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    #setting the author of the post equal to the current logged in user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    #users can only update posts if they are the author
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('home')  #redirect to home after delete a post

    #users can delete post only if they are the authors
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
            
    
class ProfileDetailView(DetailView):
    context_object_name = 'profile_detail'
    template_name = 'post/profile_detail.html'
    model = Post

    
def search_user(request):
    if request.method == "POST":
        
        searched = request.POST.get('searched')
        data = Post.objects.filter(title__icontains=searched)
        context = {
            'searched': searched,
            'posts': data
        }
        #user = get_object_or_404(User, username=self.kwargs.get('username'))
        return render(request, 'post/search_user.html', context)
    else:
        return render(request, 'post/search_user.html')


def post_view(request):
    qs = Post.objects.all()
    user = request.user
    context = {
        'qs':qs,
        'user':user,
    }
    return render(request, 'post/home.html', context)


def like_post(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post_objj = Post.objects.get(id=post_id)

        if user in post_objj.liked.all():
            post_objj.liked.remove(user)
        else:
            post_objj.liked.add(user)

        like, created = Like.objects.get_or_create(user=user, post_id=post_id)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()
    return redirect('/')


class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        followers = profile.followed.all()
        
        context = {
            'profile':profile,
            'followers':followers,
            
        }
        #print(followers.user.first_name)
        return render(request, 'post/profile_list.html', context)


def followed_accounts(request):
    followed_users_list = []
    followed_users = Profile.objects.filter(followed=request.user)
    for user in followed_users:
        user_list = User.objects.get(username=user.user)
        followed_users_list.append(user_list)
        print(followed_users)

    username_profile = []
    username_profile_list = []
    for users in followed_users_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(user_id=ids)
        username_profile_list.append(profile_lists)

    data = list(chain(*username_profile_list))

    context = {
        'data': data,
    }
    return render(request, 'post/followed_accounts.html', context)
