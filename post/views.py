from django.shortcuts import render, redirect
from .models import PostModel, CommentModel
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def home(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            all_post = PostModel.objects.all().order_by('-created_at')
            return render(request, 'post/post.html', {'posts': all_post})
        else:
            return redirect('sign_in')


def write(request): # 게시글 작성 페이지
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return render(request, 'post/new_post.html')
        else:
            return redirect('/sign-in')

    elif request.method == 'POST':
        user = request.user
        new_post = PostModel()
        new_post.author = user
        new_post.content = request.POST.get('comment','')
        new_post.save()
        return redirect('/post')


def my_profile(request): #나의 프로필 페이지
    return render(request, 'post/my_profile.html')


def detail_post(request, id):
    my_post = PostModel.objects.get(id=id)
    my_comment = CommentModel.objects.filter(post_id=id).order_by('-created_at')
    return render(request, 'post/post_detail.html', {'post': my_post, 'comment': my_comment})


@login_required
def delete_post(request, id):
    my_post = PostModel.objects.get(id=id)
    my_post.delete()
    return redirect('/')
