"""TodayProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import today.views
import account.views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',today.views.home,name="home"),
    path('postDetail/<int:post_id>',
         today.views.postDetail, name="postDetail"),
    path('createPost',
         today.views.createPost, name="createPost"),
    path('newPost', today.views.newPost, name="newPost"),
    path('addSchedule/<int:post_id>', today.views.addSchedule, name="addSchedule"),    
    path('createSchedule/<int:post_id>', today.views.createSchedule, name="createSchedule"),
    path('deleteSchedule/<int:post_id>/<int:schedule_id>', today.views.deleteSchedule, name="deleteSchedule"),
    path('deleteNewSchedule/<int:post_id>/<int:schedule_id>', today.views.deleteNewSchedule, name="deleteNewSchedule"),
    path('updateSchedule/<int:post_id>', today.views.updateSchedule, name="updateSchedule"),
    path('editPost/<int:post_id>', today.views.editPost, name="editPost"),
    path('updatePost/<int:post_id>', today.views.updatePost, name="updatePost"),
    path('deletePost/<int:post_id>', today.views.deletePost, name="deletePost"),
    path('hashtagFilter', today.views.hashtagFilter, name="hashtagFilter"),
    path('account/signup', account.views.signup, name="signup"),
    path('account/login', account.views.login_view, name="login"),
    path('account/logout', account.views.logout_view, name="logout"),
    path('mypage', account.views.mypage, name="mypage"),
    path('bookmark',today.views.bookmark, name="bookmark"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
