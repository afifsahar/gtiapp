from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.validators import validate_email
from .models import *


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = User.objects.get(
            username=user.username, email=user.email).first_name
        self.fields['last_name'].initial = User.objects.get(
            username=user.username, email=user.email).last_name
        self.fields['username'].initial = User.objects.get(
            username=user.username, email=user.email).username
        self.fields['email'].initial = User.objects.get(
            username=user.username, email=user.email).email

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'firstname', 'type': "text", 'class': 'validate',
               'name': "first_name", }
    ), required=True, max_length=50, initial=None)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'lastname', 'type': "text", 'class': 'validate',
               'name': "last_name", }
    ), required=True, max_length=50, initial=None)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'id': 'email', 'type': "email", 'class': 'validate',
               'name': "email"}
    ), required=True, max_length=50, initial=None)
    username = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'username', 'type': "text", 'class': 'validate',
               'name': "username"}
    ), required=True, max_length=50, initial=None)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        username_qs = User.objects.filter(
            username=username).exclude(username=username)
        if username_qs.exists():
            raise forms.ValidationError(
                'Username telah digunakan oleh pengguna lain')
        email = self.cleaned_data.get('email')
        try:
            eml = validate_email(email)
        except:
            raise forms.ValidationError('Format Email Salah')
        email_qs = User.objects.filter(email=email).exclude(username=username)
        if email_qs.exists():
            raise forms.ValidationError(
                'Alamat email telah terdaftar oleh pengguna lain')
        return super(UserProfileForm, self).clean(*args, **kwargs)


class UserProfilePhotoForm(forms.ModelForm):

    class Meta:
        model = user_profile
        fields = ['userPhoto']
        widgets = {
            'userPhoto': forms.FileInput(),
        }

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     super(UserProfilePhotoForm, self).__init__(*args, **kwargs)
    #     self.fields['userPhoto'].initial = user_profile.objects.get(
    #         userProfile=user.user).userPhoto

    # userPhoto = forms.ImageField(widget=forms.FileInput(attrs={
    #     'id': 'userPhoto', 'help text': 'Pilih Gambar', 'name': 'userPhoto', 'label': 'select profile picture'}
    # ), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["userPhoto"].widget.attrs.update(
            {'id': 'userPhoto', 'help text': 'Pilih Gambar', 'name': 'userPhoto', 'label': 'select profile picture', 'required': False,})
