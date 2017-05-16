from django.contrib.gis.db import models


class BicycleParking(models.Model):

    class Meta:
        verbose_name_plural = 'bicycle parking'

    capacity = models.IntegerField()
    geom = models.PointField(srid=4326)

    def __str__(self):
        return f'Bicycle parking ({self.capacity})'
