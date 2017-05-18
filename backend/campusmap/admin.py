from django.contrib.gis.admin import OSMGeoAdmin

from arcutils.admin import cas_site as site

from .bicycles.models import BicycleParking, BicycleRoute
from .buildings.models import Building


site.register((BicycleParking, BicycleRoute, Building), OSMGeoAdmin)
