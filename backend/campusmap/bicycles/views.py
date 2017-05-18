from ..views import ModelViewSet

from .models import BicycleParking, BicycleRoute
from .serializers import BicycleParkingSerializer, BicycleRouteSerializer


class BicycleParkingViewSet(ModelViewSet):

    queryset = BicycleParking.objects.all()
    serializer_class = BicycleParkingSerializer


class BicycleRoutesViewSet(ModelViewSet):

    queryset = BicycleRoute.objects.all()
    serializer_class = BicycleRouteSerializer
