from arcutils.admin import cas_site as site

from .buildings.models import Building


site.register(Building)
