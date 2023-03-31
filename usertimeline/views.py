from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import HttpResponseNotFound, JsonResponse
from users.forms import CustomAuthenticationForm
from usertimeline.models import Post, Comment, Notification
from users.models import User
from django.db.models import Q
from users.utils import get_suggestions
from django.core.cache import cache

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        form = CustomAuthenticationForm
        followed = request.user.profile.follows.all()
        posts = []
        for i in followed:
            if i.post.all().exists():
                posts += [i for i in i.post.all()]
        posts += [i for i in request.user.post.all() if i]
        suggestions = cache.get_or_set('suggestions', get_suggestions(
            request.user.username), version=request.user.id)
        return render(request, 'usertimeline/userfeed.html', {'form': form, 'posts': posts, 'suggestions': suggestions})
    else:
        return redirect('userlogin')


def about(request):
    return render(request, 'usertimeline/about.html')


@login_required
def add_comment(request):
    try:
        post_id = request.POST.get('post', None)
        comment = request.POST.get('comment', None)
        if comment and len(comment) >= 3 and comment != "" and post_id:
            post = Post.objects.select_related('user').get(id=post_id)
            Comment.objects.create(
                post=post, comment=comment, user=request.user)
            Notification.objects.create(
                receiver=post.user, sender=request.user, noti_type="3", post=post)
            return render(request, 'usertimeline/partials/comments.html', {'comments': post.comments.all(), 'post': post})
    except Exception:
        return HttpResponseNotFound()


@login_required
def reply_comment(request):
    try:
        comment_id = request.POST.get('comment', None)
        reply = request.POST.get('reply', None)
        if comment_id and reply != "" and len(reply) >= 2:
            comment = Comment.objects.select_related(
                'user', 'reply').get(id=comment_id)
            user = request.user
            notification = f'{comment.user} replied to your comment. "{reply[:20]}"'
            Comment.objects.create(
                comment=reply, user=user, reply=comment, post=comment.post)
            Notification.objects.create(
                receiver=comment.user, sender=user, noti_type="4", notification=notification, post=comment.post)
            return render(request, 'usertimeline/partials/reply.html', {'comment': comment})
    except Exception:
        return HttpResponse('Error occured')


@login_required
def like_comment(request):
    try:
        comment_id = request.POST.get('comment', None)
        if comment_id:
            comment = Comment.objects.prefetch_related(
                'post', 'user').get(id=comment_id)
            user = request.user
            if user in comment.likes.all() and user.is_authenticated:
                comment.likes.remove(user)
                comment.save()
                return HttpResponse(f'{comment.get_likes().count()} <i class="fa-solid fa-heart fa-1x mx-1"></i>')
            else:
                comment.likes.add(user)
                notification = f'{comment.user} liked your comment. "{comment.comment}"'
                Notification.objects.create(
                    receiver=comment.user, sender=user, post=comment.post, noti_type="5", notification=notification)
                comment.save()
                return HttpResponse(f'{comment.get_likes().count()} <i class="fa-solid fa-heart fa-1x mx-1 text-danger"></i>')
    except Exception:
        return HttpResponseNotFound()


@login_required
def like_post(request):
    try:
        post_id = request.POST.get('post', None)
        if post_id:
            post = Post.objects.get(id=post_id)
            user = request.user
            if user in post.likes.all() and user.is_authenticated:
                post.likes.remove(user)
                post.save()
                return HttpResponse(f'<i class="fa-solid fa-heart fa-1x mx-1"></i> <b class="mx-1 d-block text-black-50">{post.get_likes()} likes</b>')
            else:
                post.likes.add(user)
                Notification.objects.create(
                    receiver=post.user, sender=user, noti_type="2", post=post)
                post.save()
                return HttpResponse(f'<i class="fa-solid fa-heart fa-1x mx-1 text-danger"></i> <b class="mx-1 d-block text-black-50">{post.get_likes()} likes</b>')
    except Exception:
        return HttpResponseNotFound()


@login_required
def read_notification(request, user):
    if request.method == 'POST':
        user_check = get_object_or_404(User, username=user)
        if request.user == user_check:
            Notification.objects.filter(
                receiver=request.user, is_seen=False).update(is_seen=True)
            return render(request, 'usertimeline/partials/notifications.html')
    else:
        return HttpResponseNotFound()


@login_required
def search_users(request):
    if request.method == "POST":
        query = request.POST.get('query', False)
        if query and len(query) >= 3:
            search_results = User.objects.prefetch_related('profile').filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)

            )
            return render(request, 'usertimeline/partials/search.html', {'searched': search_results})
        else:
            return HttpResponse()
    else:
        return HttpResponseNotFound()


@login_required
def posts(request):
    if request.method == "POST":
        caption = request.POST.get('caption', False)
        post_image = request.FILES.get('post-image')
        if caption and post_image:
            Post.objects.create(
                image=post_image, user=request.user, caption=caption)
            followed = request.user.profile.follows.all()
            posts = []
            for i in followed:
                if i.post.all().exists():
                    posts += [i for i in i.post.all()]
            posts += [i for i in request.user.post.all() if i]
            return render(request, 'usertimeline/partials/posts.html', {'posts': posts})
    else:
        return HttpResponseNotFound()


def delete_post(request, user, post_id):
    if request.method == "POST":
        try:
            user = User.objects.get(username=user)
            post = Post.objects.get(id=post_id)
            if user == request.user and post:
                post.delete()
                followed = request.user.profile.follows.all()
                posts = []
                for i in followed:
                    if i.post.all().exists():
                        posts += [i for i in i.post.all()]
                posts += [i for i in request.user.post.all() if i]
                return render(request, 'usertimeline/partials/posts.html', {'posts': posts})
        except Exception:
            return HttpResponseNotFound()
