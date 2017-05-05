from django.conf.urls import url

from .map.views import MapView


urlpatterns = [
    url(r'^$', MapView.as_view(), name='map'),
]
