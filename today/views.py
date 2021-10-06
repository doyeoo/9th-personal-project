from datetime import time
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils import timezone
from .forms import *
import json
from django.http import HttpResponse
from django.views.decorators.http import require_POST
# Create your views here.

def home(request):
    post=Post.objects
    return render(request, 'home.html', {'posts':post})

@login_required
def createPost(request):
    new_post = Post()
    new_post.title = request.POST.get('title')
    new_post.author = request.user
    new_post.pub_date = timezone.now()
    new_post.body = request.POST.get('body')
    new_post.image=request.FILES.get('image')    
    new_post.save()
    hashtags = request.POST.get('hashtags')
    hashtag = hashtags.split('#')
    for tag in hashtag:
        hashtag = Hashtag.objects.get_or_create(hashtag_name=tag)
        new_post.hashtag.add(hashtag[0])
    
    return redirect('addSchedule', new_post.id)

def newPost(request):
    return render(request, 'newPost.html')

def postDetail(request, post_id):
    post_detail = get_object_or_404(Post, pk=post_id)
    hashtag = post_detail.hashtag.all()
    bookmark=post_detail.bookmark.all()
    schedule=post_detail.schedules.all().order_by('start_time__hour')
    return render(request, 'postDetail.html', {'post': post_detail, 'hashtags': hashtag, 'schedules': schedule, 'bookmarks':bookmark})

def editPost(request, post_id):
    post_detail = get_object_or_404(Post, pk=post_id)
    hashtag = post_detail.hashtag.all()
    schedule=post_detail.schedules.all().order_by('start_time__hour')
    return render(request, 'editPost.html', {'post': post_detail, 'hashtags': hashtag, 'schedules': schedule})

def updatePost(request, post_id):
    post_update = get_object_or_404(Post, pk=post_id)
    post_update.title = request.POST.get('title')
    post_update.body = request.POST.get('body')   
    post_update.save()
    hashtags = request.POST.get('hashtags')
    return redirect('postDetail', post_id)

def deletePost(request, post_id):
    post_delete=get_object_or_404(Post, pk=post_id)
    post_delete.delete()
    return redirect('home')
        
def schedule(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = ScheduleForm(request.POST)
    if form.is_valid(): 
        schedule = form.save(commit=False)
        schedule.post = post
        schedule.save()
        return redirect('addSchedule', post_id)
    else:
        form = ScheduleForm()
    return redirect('home')

def addSchedule(request, post_id):
    post_detail=get_object_or_404(Post, pk=post_id)
    schedule=post_detail.schedules.all().order_by('start_time__hour')
    return render(request, 'addSchedule.html', {'post':post_detail, 'schedules':schedule})

def createSchedule(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    schedule = Schedule()
    schedule.start_time = request.POST.get('start_time')
    schedule.end_time = request.POST.get('end_time')
    schedule.contents = request.POST.get('contents')
    schedule.post = post
    schedule.save()
    return redirect('addSchedule', post_id)

def deleteNewSchedule(request, post_id, schedule_id):
    new_schedule_delete = get_object_or_404(Schedule, pk=schedule_id)
    new_schedule_delete.delete()
    return redirect('addSchedule', post_id)

def updateSchedule(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    schedule_update = Schedule()
    schedule_update.start_time = request.POST.get('start_time')
    schedule_update.end_time = request.POST.get('end_time')
    schedule_update.contents = request.POST.get('contents')
    schedule_update.post = post
    schedule_update.save()
    return redirect('editPost', post_id)

def deleteSchedule(request, post_id, schedule_id):
    schedule_delete = get_object_or_404(Schedule, pk=schedule_id)
    schedule_delete.delete()
    return redirect('editPost', post_id)

def hashtagFilter(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        hashtag = Hashtag.objects.filter(hashtag_name=keyword)
        post= Post.objects.filter(hashtag__in = hashtag)
        return render(request, 'hashtagFilter.html', {'posts':post, 'keyword':keyword})
    elif request.method == 'GET':
        return redirect('/')

@login_required
def bookmark(request): 
    if request.is_ajax(): 
        post_id = request.GET['post_id']
        post = Post.objects.get(id=post_id) 

        user = request.user 
        if post.bookmark.filter(id = user.id).exists(): 
            post.bookmark.remove(user) 
            message = "북마크 취소"
        else: 
            post.bookmark.add(user) 
            message = "북마크" 
        context = {"message":message}
        return HttpResponse(json.dumps(context), content_type='application/json')    

def comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():  # 유효성 검사
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('detail', post_id)
    else:
        form = CommentForm()
    return redirect('detail', post_id)


def addComment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        comment = Comment()
        comment.message = request.POST['message']
        comment.post = post
        comment.pub_date=timezone.now()
        comment.author = request.user
        comment.save()
        return redirect('postDetail', post_id)
    else:
        return redirect('home')

def deleteComment(request, comment_id, post_id):
    comment_delete = get_object_or_404(Comment, pk=comment_id)
    comment_delete.delete()
    return redirect('postDetail', post_id)