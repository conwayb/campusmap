from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class MapView(APIView):

    template_name = 'map.html'
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request):
        return Response()
