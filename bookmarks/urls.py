from django.conf.urls import url
from django.views.generic import TemplateView

from views import *


# site_media = os.path.join(os.path.dirname(__file__), 'static')

urlpatterns = [
    # Browsing
    url(r'^$', main_page,
        name='main'),
    url(r'^user/(\w+)/$',
        user_page,
        name='user'),

    # Session management
    url(r'^login/$',
        'django.contrib.auth.views.login',
        name='registration login'),
    url(r'^logout/$',
        logout_page,
        name='registration logout'),
    url(r'^register/$',
        register_page,
        name='registration'),
    url(r'^register/success/$',
        TemplateView.as_view(template_name='registration/register_success.html'),
        name='registration success'),

    # Account management
    url(r'^save/$',
        bookmarks_save_page,
        name='save'),
]
