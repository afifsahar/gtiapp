from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import *


class PasswordRenewForm(forms.Form):

    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'type': "password", 'id': "old_password",
               'name': 'old_password', }
    ), required=True, max_length=50, initial=None)

    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'type': "password", 'id': "new_password1",
               'name': 'new_password1', }
    ), required=True, max_length=50, initial=None)

    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'type': "password", 'id': "new_password2",
               'name': 'new_password2', }
    ), required=True, max_length=50, initial=None)

    current_password = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text", 'id': "current_password",
               'name': 'current_password', }
    ), required=True, max_length=50, initial=None)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PasswordRenewForm, self).__init__(*args, **kwargs)

        self.fields['current_password'].initial = User.objects.get(
            username=user.username, email=user.email).username


# self.fields["old_password"].widget.attrs.update(
#     {'type': "password", 'id': "old_password", 'name': 'old_password'})

# self.fields["new_password1"].widget.attrs.update(
#     {'type': "password", 'id': "new_password1", 'name': 'new_password1'})

# self.fields["new_password2"].widget.attrs.update(
#     {'type': "password", 'id': "new_password2", 'name': 'new_password2'})


    def clean(self, *args, **kwargs):
        current_password = self.cleaned_data.get('current_password')
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        # password_qs = User.objects.filter(
        #     password=current_password).exclude(username=username)
        if current_password == old_password:
            raise forms.ValidationError(
                'Password Lama salah')
        if current_password != new_password1:
            raise forms.ValidationError(
                'Password lama dan Password Baru tidak boleh sama')
        if new_password1 != new_password2:
            raise forms.ValidationError(
                'Konfirmasi Password baru salah')
        return super(PasswordRenewForm, self).clean(*args, **kwargs)
