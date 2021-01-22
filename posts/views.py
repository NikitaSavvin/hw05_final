from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse

from .forms import PostForm, CommentForm
from .models import Group, Post, Follow, Comment, User


def paginators(request, paginator):
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page


def index(request):
    post_list = Post.objects.select_related('group')
    paginator = Paginator(post_list, 10)
    page = paginators(request, paginator)
    return render(
                request,
                'posts/index.html',
                {'page': page, 'paginator': paginator}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page = paginators(request, paginator)
    return render(
                request,
                'group.html',
                {'group': group, 'paginator': paginator, 'page': page}
    )


@login_required
def post_new(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('index')
    return render(request, 'posts/post_new.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'posts/profile.html',
        {'author': user, 'page': page, 'paginator': paginator}
    )


def post_view(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    form = CommentForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
    return render(
        request,
        'posts/post.html',
        {'post': post, 'author': post.author, 'form':form}
    )


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username) 
    profile = get_object_or_404(User, username=post.author) 
    if request.user != profile:
        return redirect('post', username=username, post_id=post_id)
    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
    if form.is_valid():
        form.save()
        return redirect(
            'post', username=request.user.username, post_id=post_id
        )
    return render(request, 'posts/post_new.html', {'form': form, 'post': post},)


def page_not_found(request, exception):
    return render(
        request, 
        "misc/404.html", 
        {"path": request.path}, 
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    form = CommentForm(request.POST or None)
    if not form.is_valid():
        return render(request, "posts/post.html", {'post': post, 'form ': form })
    comments = form.save(commit=False)
    comments.author = request.user
    comments.post = post
    form.save()
    return redirect(reverse('post', args= [username,  post_id]))
    

@login_required
def follow_index(request):
    follow_list = []
    follow_list_id = Follow.objects.filter(user=request.user).in_bulk()
    for n in follow_list_id:
        follow_list.append(follow_list_id[n].author)
    post_list = Post.objects.filter(author__in=follow_list)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number) 
    return render(
        request, 
        'posts/follow.html', {
            'page': page,
            'paginator': paginator,
        }
    )

@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author and not Follow.objects.filter(
        user=request.user, author=author).exists():
        Follow(user=request.user, author=author).save()
    return profile(request, username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    if Follow.objects.filter(
        user=request.user, author=author
    ).exists():
        Follow(user=request.user, author=author).delete()
    return profile(request, username)
    