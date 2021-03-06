from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm


def post_list(request):
    search = request.GET.get("search", "")
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    if search != "":
        posts = posts.filter(text__icontains=search) | posts.filter(title__icontains=search)
    return render(request, 'blog/post_list.html', {'posts': posts, "search": search})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.user.is_anonymous:
        return redirect('login')

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
    return redirect("/")


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def login_url(request):
    if request.method == "POST":
        print("Our user wants to post something", request.POST)
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        if user is None:
            print("Password is incorrect")
        else:
            print("Everything is fine")
            login(request, user)
            return redirect("/")

    return render(request, "blog/login.html")


def logout_url(request):
    logout(request)
    return redirect("/")
