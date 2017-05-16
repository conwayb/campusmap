from django.contrib.gis.admin import OSMGeoAdmin

from arcutils.admin import cas_site as site

from .bicycles.models import BicycleParking
from .buildings.models import Building


site.register((BicycleParking, Building), OSMGeoAdmin)
