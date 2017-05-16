from ..views import ModelViewSet

from .models import BicycleParking
from .serializers import BicycleParkingSerializer


class BicycleParkingViewSet(ModelViewSet):

    queryset = BicycleParking.objects.all()
    serializer_class = BicycleParkingSerializer
