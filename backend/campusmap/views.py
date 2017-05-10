from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView


class AppConfigView(APIView):

    def get(self, request):
        return Response({
            'bing_maps_key': settings.MAP.bing.key,
        })
