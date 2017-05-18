from django.db.models import Q

from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from ..buildings.models import Building
from ..buildings.serializers import BuildingSerializer


class SearchView(APIView):

    def get(self, request):
        term = request.query_params.get('q', '').strip()
        if not term:
            raise ParseError('Missing query parameter: q')

        query = Building.objects.filter(Q(name__icontains=term) | Q(code__icontains=term))
        serializer = BuildingSerializer(query, many=True)
        results = serializer.data
        count = len(results)

        if not len(results):
            raise NotFound(f'No results found matching term: {term}')

        return Response({
            'results': results,
            'count': count
        })
