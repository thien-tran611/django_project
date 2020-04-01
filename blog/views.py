from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import post


def home(request):
    context = {
        'posts': post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListview(ListView):
    model = post
    template_name = 'blog/home.html'
    context_object_name = 'posts' #<app>/<model>_<viewtype>.html
    ordering = ['-date_posted']
    paginate_by = 4


class UserPostListview(ListView):
    model = post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts' #<app>/<model>_<viewtype>.html
    #ordering = ['-date_posted']
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date_posted')


class PostDetailview(DetailView):
    model = post


class PostCreateview(LoginRequiredMixin, CreateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        #form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateview(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        #form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteview(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
