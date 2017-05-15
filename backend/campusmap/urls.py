from django.conf.urls import include, url
from arcutils.cas import urls as cas_urls

from . import views


urlpatterns = [
    url(r'^app-config$', views.AppConfigView.as_view(), name='app-config'),
    url(r'^account/', include(cas_urls)),
]
