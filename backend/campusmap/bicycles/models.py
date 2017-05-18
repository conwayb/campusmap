from django.contrib.gis.db import models


class BicycleParking(models.Model):

    class Meta:
        verbose_name_plural = 'bicycle parking'

    capacity = models.IntegerField()
    geom = models.PointField(srid=4326)

    def __str__(self):
        return f'Bicycle parking ({self.capacity})'


class BicycleRoute(models.Model):

    classification = models.CharField(max_length=255, null=True, blank=True, choices=(
        ('BKE-BLVD', 'Bike Boulevard'),
        ('BKE-BUFF', 'Buffered Bike Lane'),
        ('BKE-LANE', 'Bike Lane'),
        ('BKE-SHRD', 'Shared Roadway or Marked Bicycle Route'),
        ('BKE-TRAK', 'Cycle Track'),
        ('OTH-CONN', 'Shared Roadway Gap Connector'),
        ('OTH-SWLK', 'Sidewalk'),
        ('OTH-XING', 'Pedestrian or Bike Overpass/underpass'),
        ('PTH-LOMU', 'Local Multiuse Path'),
        ('PTH-REMU', 'Regional Multiuse Path'),
        ('SHL-WIDE', 'Wide Shoulder'),
    ))
    bike_there_classification = models.CharField(max_length=255, null=True, blank=True, choices=(
        ('CA', 'Caution Area'),
        ('HT', 'High Traffic'),
        ('MT', 'Medium Traffic'),
        ('LT', 'Light Traffic'),
    ))
    geom = models.LineStringField(srid=4326)

    def __str__(self):
        classification = self.get_classification_display() or 'N/A'
        bike_there_classification = self.get_bike_there_classification_display() or 'N/A'
        return f'{classification} ({bike_there_classification})'
