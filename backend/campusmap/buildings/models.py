import posixpath

from django.contrib.gis.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Building(models.Model):

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)

    code = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    geom = models.MultiPolygonField(srid=4326)

    @property
    def building_href(self):
        if not self.code:
            return None
        return posixpath.join('http://www.pdx.edu/floorplans/buildings/', self.code.lower())

    @classmethod
    def normalize_address(cls, address):
        if not address:
            return None

        parts = address.split()

        number, prefix, street, *rest = parts
        prefix = prefix.upper()
        street = street.lower() if street[0].isdecimal() else street.title()

        parts = [number, prefix, street]
        parts.extend(part.title() for part in rest)

        normalized_address = ' '.join(parts)
        return normalized_address

    def __str__(self):
        if self.code:
            return f'{self.name} ({self.code})'
        return self.name


@receiver(pre_save, sender=Building)
def normalize_address(sender, instance, **kwargs):
    instance.address = instance.normalize_address(instance.address)
