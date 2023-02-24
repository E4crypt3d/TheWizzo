from django.urls import path
from users import views

urlpatterns = [
    path('login', views.UserLogin.as_view(), name='userlogin'),
    path('logout', views.UserLogout.as_view(), name='userlogout'),
    path('register', views.UserRegister.as_view(), name='userregister'),
    path('<str:user>/profile', views.user_profile, name='userprofile'),
    path('<str:user>/followers', views.user_followers, name='followers'),
    path('<str:user>/following', views.user_following, name='following'),
    path('<str:user>/likedposts', views.liked_posts, name='likedpost'),
    path('<str:user>/posts', views.posts, name='posts'),
    path('<str:user>/unfollow', views.unfollow_user, name='unfollow'),
    path('<str:user>/follow', views.follow_user, name='follow'),
    path('<str:user>/profile/edit', views.edit_profile, name='editprofile'),
]
