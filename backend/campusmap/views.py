from django.conf import settings

from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet as BaseModelViewSet


class ModelViewSet(BaseModelViewSet):

    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class AppConfigView(APIView):

    def get(self, request):
        return Response({
            'bing_maps_key': settings.MAP.bing.key,
        })
