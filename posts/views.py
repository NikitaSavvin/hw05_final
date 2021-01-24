from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404
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
    post = get_object_or_404(Post.objects.select_related('author'), id=post_id, author__username=username)
    post_list = post.author.posts.all()
    post_count = post_list.count()
    comments = Comment.objects.filter(post=post)
    form = CommentForm(request.POST or None)
    following = False
    if request.user.is_authenticated:
        following = request.user.follower.filter(author=post.author).exists()
    context = {
        'post': post, 'post_count': post_count, 'author': post.author,
        'comments': comments, 'form': form, 'following': following
    }
    return render(request, 'posts/post.html', context)



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
    if form.is_valid():
        form = form.save(commit=False)
        form.author = post.author
        form.post = post
        form.save()
        return redirect(reverse('post', args= [username,  post_id]))
    return redirect(reverse('post', args= [username,  post_id]))
    

@login_required
def follow_index(request):
    user = request.user
    list = user.follower.all().values('author')
    follow_post_list = Post.objects.filter(author__in=list).order_by(
        '-pub_date')
    paginator = Paginator(follow_post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number) 
    return render(
        request, 
        'includes/follow.html', {
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
        return redirect('profile', username=username)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('profile', username=username)
