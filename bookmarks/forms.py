import re

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=30
    )
    email = forms.EmailField(
        label='Email'
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='Password (Again)',
        widget=forms.PasswordInput()
    )

    # password validation:
    def cleaned_password2(self):
        # all valid values are accessible trough self.clean_data
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    # username validation
    def cleaned_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')


class BookmarkSaveForm(forms.Form):
    url = forms.URLField(
        label='URL',
        widget=forms.TextInput(attrs={'size': 64})
    )
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'size': 64})
    )
    tags = forms.CharField(
        label='Tags',
        widget=forms.TextInput(attrs={'size': 64})
    )
