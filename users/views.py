from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from users.models import User
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomProfileEditForm
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
# Create your views here.


class UserLogin(LoginView):
    template_name = 'users/login-default.html'
    authentication_form = CustomAuthenticationForm
    success_url = '/'
    next_page = '/'
    extra_context = {'login': True}

    def form_valid(self, form):
        if form.data.get('remember_me', False):
            self.request.session.set_expiry(345600)
        return super().form_valid(form)


class UserLogout(LogoutView):
    next_page = '/'


class UserRegister(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/login-default.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["register"] = True
        return context


@login_required
def user_profile(request, user):
    try:
        user = User.objects.select_related('profile').get(username=user)
    except Exception:
        return HttpResponse('<div class="text-danger">Error occured</div>')
    return render(request, 'users/userprofile.html', {'puser': user})


@login_required
def user_followers(request, user):
    try:
        user = User.objects.select_related('profile').get(username=user)
    except Exception:
        return HttpResponse('<div class="text-danger">Error occured</div>')
    return render(request, 'users/partials/followers.html', {'puser': user})


@login_required
def user_following(request, user):
    try:
        user = User.objects.select_related('profile').get(username=user)
    except Exception:
        return HttpResponse('<div class="text-danger">Error occured</div>')
    return render(request, 'users/partials/following.html', {'puser': user})


@login_required
def liked_posts(request, user):
    try:
        user = User.objects.select_related('profile').get(username=user)
    except Exception:
        return HttpResponse('<div class="text-danger">Error occured</div>')
    return render(request, 'users/partials/liked_post.html', {'puser': user})


@login_required
def posts(request, user):
    try:
        user = User.objects.prefetch_related(
            'profile', 'post').get(username=user)
    except Exception:
        return HttpResponse('<div class="text-danger">Error occured</div>')
    return render(request, 'users/partials/posts.html', {'puser': user})


@login_required
def unfollow_user(request, user):
    cache.delete('suggestions', version=request.user.id)
    unfollow_user_id = request.POST.get('wizu', None)
    if unfollow_user_id and user:
        unfollow_user = User.objects.get(
            username=user, id=unfollow_user_id)
        user = request.user
        user.profile.follows.remove(unfollow_user)
        return redirect('wizzo-home')


@login_required
def follow_user(request, user):
    follow_user_id = request.POST.get('wizu', None)
    cache.delete('suggestions', version=request.user.id)
    if follow_user_id and user:
        follow_user = User.objects.get(username=user, id=follow_user_id)
        user = request.user
        user.profile.follows.add(follow_user)
        return HttpResponse("Followed")


@login_required
def edit_profile(request, user):
    print(user)
    user_check = User.objects.prefetch_related('profile').get(username=user)
    if user_check == request.user and request.user.is_authenticated:
        if request.method == "POST":
            if request.FILES.get('profile_pic', False):
                profile_pic = request.FILES['profile_pic']
                request.user.profile.profile_pic = profile_pic
                request.user.profile.save()
                return HttpResponse('uploaded')
            if request.POST.get('username') == request.user.username:
                post_data = request.POST.copy()
                bio = post_data.pop('bio')
                user_check.profile.bio = bio[0]
                user_check.profile.save()
                form = CustomProfileEditForm(post_data, instance=request.user)
                if form.is_valid():
                    form.save()
                    return render(request, 'users/partials/pedit.html', {'form': form})
                else:
                    return render(request, 'users/partials/pedit.html', {'form': form})
        else:
            form = CustomProfileEditForm(instance=request.user)
            return render(request, 'users/partials/pedit.html', {'form': form})
