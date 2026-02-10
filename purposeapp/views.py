# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *


def home(request):
    query = request.GET.get('q')
    photos = Photo.objects.all().order_by('-created_at')

    if query:
        photos = photos.filter(
            Q(title__icontains=query) |
            Q(tags__icontains=query)
        )

    return render(request, 'home.html', {'photos': photos})


def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'photo_detail.html', {'photo': photo})


@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.owner = request.user
            photo.save()
            return redirect('home')
    else:
        form = PhotoForm()

    return render(request, 'upload_photo.html', {'form': form})


@login_required
def edit_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)

    if photo.owner != request.user:
        return redirect('home')

    form = PhotoForm(request.POST or None, request.FILES or None, instance=photo)
    if form.is_valid():
        form.save()
        return redirect('photo_detail', pk=pk)

    return render(request, 'edit_photo.html', {'form': form})



@login_required
def react_photo(request, pk, value):
    photo = get_object_or_404(Photo, pk=pk)

    
    if photo.owner == request.user:
        return redirect('photo_detail', pk=pk)

    if value == 1:
       
        Like.objects.get_or_create(
            user=request.user,
            photo=photo
        )
        Dislike.objects.filter(
            user=request.user,
            photo=photo
        ).delete()

    elif value == 0:
       
        Dislike.objects.get_or_create(
            user=request.user,
            photo=photo
        )
        Like.objects.filter(
            user=request.user,
            photo=photo
        ).delete()

    return redirect('photo_detail', pk=pk)


@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if form.is_valid():
        form.save()
        return redirect('profile')

    return render(request, 'profile.html', {'form': form})


def signup(request):
    form = UserCreationForm(request.POST or None)

    for field in form.fields.values():
        field.widget.attrs.update({
            'class': 'w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-black'
        })

    if form.is_valid():
        form.save()
        return redirect('login')

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def delete_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)

    if photo.owner != request.user:
        return redirect('photo_detail', pk=pk)

    photo.delete()
    return redirect('home')
