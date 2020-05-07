from itertools import chain
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, Category
from users.models import Profile
from .forms import CommentForm
from django.db.models import Q
from django.contrib import messages, auth
from django.http import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

def list_of_post_by_category(request, category_slug):
    categories = Category.objects.all()
    post = Post.objects.filter()
    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        post = post.filter(category = category)
    template = 'blog/list_of_post_by_category.html'
    context = {'categories': categories, 'post': post, 'category': category,}
    return render(request, template, context)

def home(request):
	context={
		'posts':Post.objects.all(),
	}
	return render(request, 'blog/home.html', context)

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 3

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'category', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
    	post = self.get_object()
    	if self.request.user == post.author:
    		return True
    	return False

def add_comment_to_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect('post-detail', pk=post.pk)
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.approve()
	return redirect('post-detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.delete()
	return redirect('post-detail', pk=comment.post.pk)

def search(request):
	template_name = "blog/home.html"
	query = request.GET.get("q")
	if query:
		results = Post.objects.filter(Q(title__icontains=query)|Q(content__icontains=query)).order_by('-date_posted')

	else:
		return render(request, template_name)

	context = {
		'posts':results,
		'query':query,
		'title':'Search results for ' + query
		# 'items':pages[0],
		# 'page_range':pages[1],
	}

	return render(request, template_name, context)