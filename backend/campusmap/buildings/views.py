from ..views import ModelViewSet

from .models import Building
from .serializers import BuildingSerializer


class BuildingsViewSet(ModelViewSet):

    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
