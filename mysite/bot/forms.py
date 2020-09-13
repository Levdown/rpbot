from django import forms
from .models import Video, Profile


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('name', 'discription', 'url_video', 'video')
        widgets = {'name': forms.TextInput,}

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('external_id', 'name')
        widgets = {'name': forms.TextInput}