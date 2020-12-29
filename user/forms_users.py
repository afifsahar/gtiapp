from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.validators import validate_email
from .models import user_profile, User


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)
    grs = [(gr.id, gr) for gr in Group.objects.all()]
    grs.insert(0, ('', '--- authorization ---'))
    name = forms.ChoiceField(choices=grs, initial='jabatan',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {'id': 'jabatan', 'class': "form-control", 'help text': 'Pilih Jabatan', 'name': 'jabatan'})


class UserRegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'password', 'confirm_password')

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'firstname', 'type': "text", 'placeholder': 'Firstname', 'autocomplete': 'off',
               'name': "first_name"}
    ), required=True, max_length=50)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'lastname', 'type': "text", 'placeholder': 'Lastname', 'autocomplete': 'off',
               'name': "last_name"}
    ), required=True, max_length=50)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'id': 'email', 'type': "email", 'placeholder': 'Email', 'autocomplete': 'off',
               'name': "email"}
    ), required=True, max_length=50)
    username = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'username', 'type': "text", 'placeholder': 'Username', 'autocomplete': 'off',
               'name': "username"}
    ), required=True, max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'id': 'password', 'type': "password", 'placeholder': 'Password', 'autocomplete': 'off',
               'name': "password"}
    ), required=True, max_length=50)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'id': 'confirm_password', 'type': "password", 'placeholder': 'Confirm Password', 'autocomplete': 'off',
               'name': "confirm_password"}
    ), required=True, max_length=50)

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        password_qs = User.objects.filter(password=password)
        if password_qs.exists():
            raise forms.ValidationError(
                'Password telah digunakan oleh pengguna lain')
        if password != confirm_password:
            raise forms.ValidationError(
                'Password dan Password Konfirmasi tidak sama')

        username = self.cleaned_data.get('username')
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError(
                'Username telah digunakan oleh pengguna lain')

        email = self.cleaned_data.get('email')
        try:
            eml = validate_email(email)
        except:
            raise forms.ValidationError('Format Email Salah')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError(
                'Alamat email telah terdaftar oleh pengguna lain')

        return super(UserRegistrationForm, self).clean(*args, **kwargs)


class UserLoginForm(forms.Form):

    # class Meta:
    #     model = User
    #     fields = ('username', 'password',)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'username', 'type': "text", 'name': "username", 'placeholder': 'Username', 'autocomplete': 'off'}), required=True, max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'id': 'password', 'type': "password", 'name': "password", 'placeholder': 'Password', 'autocomplete': 'off'}), required=True, max_length=50)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(
                    'Username dan Password tidak sesuai')
        return super(UserLoginForm, self).clean(*args, **kwargs)
