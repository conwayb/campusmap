from django.apps import AppConfig


class DefaultAppConfig(AppConfig):

    name = 'campusmap'

    def ready(self):
        from django.contrib.gis.db.models import GeometryField
        from rest_framework.serializers import ModelSerializer
        from campusmap.serializers import GeoJSONField

        # This makes DRF use our GeoJSON field serializer by default for
        # all geometry field types.
        ModelSerializer.serializer_field_mapping[GeometryField] = GeoJSONField
