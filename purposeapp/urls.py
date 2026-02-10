from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('photo/<int:pk>/', views.photo_detail, name='photo_detail'),
    path('photo/<int:pk>/edit/', views.edit_photo, name='edit_photo'),
    path('react/<int:pk>/<int:value>/', views.react_photo, name='react_photo'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/signup/', views.signup, name='signup'),
    path('photo/<int:pk>/delete/', views.delete_photo, name='delete_photo'),


]
