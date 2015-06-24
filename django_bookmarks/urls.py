import os.path

from django.conf.urls import url
from django.views.generic import TemplateView

from bookmarks.views import *

site_media = os.path.join(os.path.dirname(__file__), 'static')

urlpatterns = [
    # Browsing
    url(r'^$', main_page),
    url(r'^user/(\w+)/$', user_page),

    # Session management
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
    url(r'^register/$', register_page),
    url(r'^register/success/$', TemplateView.as_view(template_name='registration/register_success.html')),

    # Account management
    url(r'^save/$', bookmarks_save_page),
]
