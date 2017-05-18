from ..importer import GeoJSONImporter, RLISShapefileImporter

from .models import BicycleParking, BicycleRoute


class BicycleParkingImporter(GeoJSONImporter):

    abstract = False
    model = BicycleParking

    field_name_map = {
        'capacity': 'Capacity',
        'geom': 'POINT',
    }


class BicycleRouteImporter(RLISShapefileImporter):

    abstract = False
    model = BicycleRoute

    field_name_map = {
        'classification': 'BIKETYP',
        'bike_there_classification': 'BIKETHERE',
        'geom': 'LINESTRING',
    }

    filters = (
        (lambda data: data['classification'] or data['bike_there_classification']),
    )
