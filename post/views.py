from django.shortcuts import render, redirect
from .models import PostModel, CommentModel
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def home(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            all_post = PostModel.objects.all().order_by('-created_at')
            all_comment = CommentModel.objects.all().order_by('-created_at')
            return render(request, 'post/post.html', {'posts': all_post, 'comment': all_comment})
        else:
            return redirect('sign_in')


def write(request): # 게시글 작성 페이지
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return render(request, 'post/write.html')
        else:
            return redirect('/sign-in')

    elif request.method == 'POST':
        user = request.user
        new_post = PostModel()
        new_post.author = user
        new_post.content = request.POST.get('content','')
        new_post.title = request.POST.get('title','')
        new_post.image_link = request.POST.get('image_link', '')
        new_post.images = request.FILES['images']
        new_post.save()
        return redirect('/')


def my_profile(request): #나의 프로필 페이지
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            my_id = request.user.id
            my_post = PostModel.objects.filter(author_id=my_id).order_by('-created_at')
            return render(request, 'post/my_profile.html', {'posts': my_post})
        else:
            return redirect('/sign-in')

    elif request.method == 'POST':
        user = request.user
        # 이후 추가 작성 예정


def detail_post(request, id):
    my_post = PostModel.objects.get(id=id)
    my_comment = CommentModel.objects.filter(post_id=id).order_by('-created_at')
    return render(request, 'post/post_detail.html', {'post': my_post, 'comment': my_comment})


@login_required
def write_comment(request, id):
    if request.method == 'POST':
        comment = request.POST.get("comment",'')
        last_updated_at = request.POST.get('create_at')
        current_post = PostModel.objects.get(id=id)
        if comment == '':
            return redirect('/')
        post_comment = CommentModel()
        post_comment.comment = comment
        post_comment.post = current_post
        post_comment.author = request.user
        post_comment.last_updated_at = last_updated_at
        print(last_updated_at)
        print(comment)
        post_comment.save()
        return redirect('/')


@login_required
def delete_comment(request, id):
    my_post = CommentModel.objects.get(id=id)
    my_post.delete()
    return redirect('/')


@login_required
def delete_post(request, id):
    my_post = PostModel.objects.get(id=id)
    my_post.delete()
    return redirect('/')
