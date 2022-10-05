from django.shortcuts import render, redirect
from .models import PostModel, CommentModel
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
import os
from uuid import uuid4
from B2_instagramclone.settings import MEDIA_ROOT


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
    return render(request, 'post/write.html')


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
        return redirect(f'/post/{post_comment.post_id}')


@login_required
def delete_comment(request, id):
    my_post = CommentModel.objects.get(id=id)
    my_post.delete()
    return redirect(f'/post/{my_post.post_id}')


@login_required
def edit_post(request, id):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            current_post = PostModel.objects.get(id=id)
            return render(request, 'post/edit_post.html', {'post': current_post})
        else:
            return redirect('/sign-in')

    elif request.method == 'POST':
        edited_post = PostModel.objects.get(id=id)

        edited_post.content = request.POST.get('content','')
        edited_post.title = request.POST.get('title','')
        edited_post.images = request.FILES['images']
        edited_post.save()

        return redirect('/')


@login_required
def delete_post(request, id):
    my_post = PostModel.objects.get(id=id)
    my_post.delete()
    return redirect('/')

class UploadPost(APIView):  # 게시글 업로드
    def post(self, request):
        file = request.FILES['file']

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        image = uuid_name
        title = request.data.get('title')
        content = request.data.get('content')
        created_at = request.data.get('created_at')
        updated_at = request.data.get('updated_at')

        PostModel.objects.create(author=request.user, title=title, content=content, image=image, created_at=created_at, updated_at=updated_at)

        return Response(status=200)
