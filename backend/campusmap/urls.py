from django.conf.urls import include, url
from django.http import HttpResponse

from arcutils import admin
from arcutils.cas import urls as cas_urls
from arcutils.drf.routers import DefaultRouter

from . import views
from .buildings.views import BuildingsViewSet


urlpatterns = [
    url(r'^$', lambda r: HttpResponse('Nothing to see here'), name='home'),
    url(r'^app-config$', views.AppConfigView.as_view(), name='app-config'),
    url(r'^admin/', include(admin.cas_site.urls)),
    url(r'^account/', include(cas_urls)),
]


router = DefaultRouter()
router.register(r'buildings', BuildingsViewSet)
urlpatterns += router.urls
