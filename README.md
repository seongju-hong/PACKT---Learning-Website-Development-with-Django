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
django_bookmarks/urls.py
``` Python
urlpatterns = [
    url(r'^$', main_page),
    url(r'^user/(\w+)/$', user_page),
]
```
## Chapter 4: User Registration and Management
### Creating the Login Page
Creating the login page like mentioned in the book will lead to an error trying to log in. The correct template is as follows:

templates/registration/login.html
``` Html
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
