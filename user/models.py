from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    class Meta:
        db_table = 'my_insta'

    # user_id = models.EmailField(max_length=50, default='')
    # user_phone = models.CharField(max_length=50, Null=True)
    user_nick_name = models.CharField(("닉네임"), max_length=100, default='')
    # user_password = models.CharField(max_length=20,default='')
    user_create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_id} / {self.user_nick_name}'