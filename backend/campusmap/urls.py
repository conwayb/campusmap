from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.AppConfigView.as_view(), name='app-config'),
]
