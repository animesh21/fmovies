"""
This is the url configuration file of the project.
author info@asquarexpert.com
"""

from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth.models import Group
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'FantasyMovie Admin panel'
# admin.site.unregister(Group)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'web',include('urls.web_urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
