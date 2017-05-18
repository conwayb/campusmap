from ..importer import GeoJSONImporter

from .models import BicycleParking


class BicycleParkingImporter(GeoJSONImporter):

    abstract = False
    model = BicycleParking

    field_name_map = {
        'capacity': 'Capacity',
        'geom': 'POINT',
    }
