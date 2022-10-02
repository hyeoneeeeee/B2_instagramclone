from django.urls import path
from user import views


urlpatterns = [
    path('sign_in/', views.sign_in_view, name='sign_in'),
    path('sign_up/', views.sign_up_view, name='sign_up'),
]