from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('write/', views.write, name='write'),
    path('post/<int:id>', views.detail_post, name='detail-post'),
    path('myprofile/', views.my_profile, name='my-profile'),
]