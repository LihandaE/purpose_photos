# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Photo, Like
from django.contrib.auth.decorators import login_required

def home(request):
    photos = Photo.objects.all().order_by('-created_at')
    return render(request, 'gallery/home.html', {'photos': photos})
def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'gallery/photo_detail.html', {'photo': photo})
@login_required
def react_photo(request, pk, value):
    photo = get_object_or_404(Photo, pk=pk)
    Like.objects.update_or_create(
        user=request.user,
        photo=photo,
        defaults={'value': value}
    )
    return redirect('photo_detail', pk=pk)

