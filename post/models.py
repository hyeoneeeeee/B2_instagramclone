# post/models.py
from django.db import models
from user.models import UserModel


# Create your models here.
class PostModel(models.Model):  # 게시물 데이터베이스 모델
    class Meta:
        db_table = "post"

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)     # 작성자 참조
    title =  models.TextField()  # 게시물 제목
    content = models.TextField()  # 게시물 내용
    image = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CommentModel(models.Model):   # 댓글 데이터베이스 모델
    class Meta:
        db_table = "comment"

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)   # 작성자와 게시물 참조
    comment = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
