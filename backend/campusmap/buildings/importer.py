from django.db import transaction
from django.db.models.signals import pre_save

from ..importer import GeoJSONImporter

from .models import Building, normalize_address


class BuildingsImporter(GeoJSONImporter):

    abstract = False
    model = Building

    field_name_map = {
        'code': 'BUILDINGID',
        'name': 'LONGNAME',
        'short_name': 'ShortName',
        'address': 'BLDG_ADDR',
        'geom': 'MULTIPOLYGON',
    }

    def pre_run(self):
        pre_save.disconnect(normalize_address, sender=Building)

    def post_run(self):
        buildings = Building.objects.all()

        self.print(f'Normalizing {self.model_name} addresses...')
        if self.real_run:
            with transaction.atomic():
                for building in buildings:
                    if self.verbose:
                        self.print(building.address, '=>', end=' ')
                    building.address = building.normalize_address(building.address)
                    building.save()

        pre_save.connect(normalize_address, sender=Building)
