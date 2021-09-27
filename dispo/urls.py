from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/create/', views.create_user),
    path('post/create/', views.create_post),
    path('users/top', views.get_top_users),
    path('users/feed/<user_id>',  views.get_list_of_posts),
    path('users/follow', views.follow_user),
]
