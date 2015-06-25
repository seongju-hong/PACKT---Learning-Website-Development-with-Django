import os.path
from django.conf.urls import url, include

# site_media = os.path.join(os.path.dirname(__file__), 'static')

urlpatterns = [
    url(r'^', include('bookmarks.urls', namespace="bookmarks")),
]
