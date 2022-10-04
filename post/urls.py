from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('write/', views.write, name='write'),
    path('post/<int:id>', views.detail_post, name='detail-post'),
    path('myprofile/', views.my_profile, name='my-profile'),
    path('post/delete/<int:id>', views.delete_post, name='delete-post'),
    path('post/comment/<int:id>', views.write_comment, name='write_comment'),
    path('post/comment/delete/<int:id>', views.delete_comment, name='write_comment'),
]