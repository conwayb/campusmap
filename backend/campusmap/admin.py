from django.contrib.gis.admin import OSMGeoAdmin

from arcutils.admin import cas_site as site

from .buildings.models import Building


site.register(Building, OSMGeoAdmin)
