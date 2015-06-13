# PACKT - Learning Website Development with Django

This repository contains my exercises from the book [Learning website development with Django](https://www.packtpub.com/web-development/learning-website-development-django), published in 2008 by [PACKT Publishing](https://www.packtpub.com/).

Unfortunately the book contains some deprecated code, in this readme I will include as much as possible of the deprecated code and the code that is used in the newer releases of Django.

## Chapter 2: Getting Started
### Creating Your First Project
#### Setting up the Database
django_bookmarks/settings.py
``` Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'bookmarksdb',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
```
## Chapter 3: Building a Social Bookmarking Application
### Models: Designing an Initial Database Schema
#### The Bookmark Data Model
bookmarks/models.py:
``` Python
from django.contrib.auth.models import User


class Bookmark(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    link = models.ForeignKey(Link)
```

``` Bash
$ python manage.py makemigrations
$ python manage.py migrate
```
### Templates: Creating a Template for the Main Page
Most of Django configuration is done with tupples since release 1.8

django_bookmarks/settings.py
``` Python
TEMPLATES = [
    {
        ...
        'DIRS': ['templates'],
        ...
    },
]
```
### Putting It All Together: Generating User Pages
the urls.py is reformed and uses a tupple of url objects.

django_bookmarks/urls.py
``` Python
urlpatterns = [
    url(r'^$', main_page),
    url(r'^user/(\w+)/$', user_page),
]
```
## Chapter 4: User Registration and Management
### Session Authentication
#### Creating the Login Page
Creating the login page like mentioned in the book will lead to an error trying to log in. The template is not changed much, it only needs an additional line with `{% csrf_token %}`. 
The correct template is as follows:

templates/registration/login.html
``` HTML5
<html>
    <head>
        <title>Django Bookmarks - User Login</title>
    </head>
    <body>
        <h1>User Login</h1>
        {% if form.has_errors %}
            <p>Your username and password didn't match.
                Please try again.</p>
        {% endif %}
        <form method="post" action=".">
            {% csrf_token %}
            <p><label for="id_username">Username:</label>
                {{ form.username }}</p>
            <p><label for="id_password">Password:</label>
                {{ form.password }}</p>
            <input type="hidden" name="next" value="/" />
            <input type="submit" value="login" />
        </form>
    </body>
</html>
```
### Improving Template Structure
This one is not really a fault but, because most major browsers nowadays support HTML5 it is save to change the `!DOCTYPE` tag.
``` HTML5
<!DOCTYPE html>
<html>
    ...
</html>
```

login.html has to get added `{% csrf_token %}` again after replacing it!

To add the stylesheet, create a directory called static in your project directory. Inside it you create the file style.css. 
To link to the stylesheet, edit templates/base.html like this:
``` HTML5
<head lang="en">
    ...
    {% load staticfiles %}
    <link rel="stylesheet" href="{% static  "style.css" %}"/>
</head>
```

do not change the urls.py file like suggested but instead make sure django_bookmarks/settings.py includes next lines:
``` Python
import os.path


STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join('static'),)
```
### User Registration
#### Designing the User Registration Form
In Django 1.8 `clean_data` is replaced by `cleaned_data`. To avoid confusion I pulled the change true to all code related.

bookmarks/forms.py
``` Python
import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password (Again)', widget=forms.PasswordInput())

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
```

bookmarks/views.py
``` Python
from bookmarks.forms import *


def register_page(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
        )
        return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/register.html', variables)
```

In /templates/registration/register.html, at the beginning of the `<form>`, the next command should be added again, `{% csrf_token %}`.

django.views.generic.simple.direct_to_template does not exist anymore, instead you have to use django.views.generic.base.TemplateView:

django_bookmarks/urls.py
``` Python
from django.views.generic import TemplateView


urlpatterns = [
    ...
    url(r'^register/success/$', TemplateView.as_view(template_name='registration/register_success.html')),
]
```