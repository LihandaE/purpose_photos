from django import forms
from .models import Photo, Profile

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'title', 'tags']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
