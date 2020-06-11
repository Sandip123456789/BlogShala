from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
#from django.http import HttpResponse

# Create your views here.
# def home(request):
#     return HttpResponse('<h1>Blog home</h1>')

# def about(request):
#     return HttpResponse('<h1>Blog about</h1>')

#Dummy data
# posts = [
#     {
#         'author': 'sandyC',
#         'title': 'Blog post 1',
#         'content': 'First post content',
#         'date_posted': 'may 29, 2020'
#     },
#     {
#         'author': 'john doe',
#         'title': 'Blog post 2',
#         'content': 'Second post content',
#         'date_posted': 'may 30, 2020'
#     }
# ]

#home function
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

#home ListView
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-posted_date']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-posted_date')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Post

#UpdateView is similar to CreateView
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:   #self.request.user this gets the currently login user
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:   #self.request.user this gets the currently login user
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About' })
