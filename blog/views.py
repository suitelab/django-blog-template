from django.shortcuts import render
from .models import Post
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, UserForm
from django.shortcuts import redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate


# Create your views here.
def post_list(request):
    post_data = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    page_data = Paginator(post_data, 5)
    page = request.GET.get('page')

    try:
        posts = page_data.page(page)
    except PageNotAnInteger:
        posts = page_data.page(1)
    except EmptyPage:
        posts = page_data.page(page_data.num_pages)

    return render(request, 'blog/post_list.html',
                  {'posts': posts, 'current_page': int(page or 1), 'total_page': range(1, page_data.num_pages + 1)})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
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


# def signup(request):
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         if form.is_valid():
#             new_user = User.objects.create_user(**form.cleaned_data)
#             login(request, new_user)
#             return redirect('index')
#     else:
#         form = UserForm()
#     return render(request, 'blog/add_user.html', {'form': form})
#
#
# def signin(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('/')
#         else:
#             return HttpResponse('로그인 실패. 다시 시도 해보세요.')
#     else:
#         form = LoginForm()
#         return render(request, 'blog/login.html', {'form': form})

