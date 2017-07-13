from collections import OrderedDict

from rest_framework.serializers import Field


class GeoJSONField(Field):

    def to_representation(self, geom):
        instance = geom._drf_serializer_instance
        feature_id = self.get_feature_id(instance)
        geometry = self.get_geometry(geom)
        properties = self.get_properties(instance)
        return OrderedDict((
            ('id', feature_id),
            ('type', 'Feature'),
            ('geometry', geometry),
            ('bbox', geom.extent if geom.coords else None),
            ('centroid', geom.centroid.coords if geom.coords else None),
            ('properties', properties),
        ))

    def get_attribute(self, instance):
        attr = super().get_attribute(instance)
        attr._drf_serializer_instance = instance
        return attr

    def get_feature_id(self, instance):
        pk = instance.pk
        name = instance._meta.verbose_name_plural.replace(' ', '-')
        return '{name}.{pk}'.format_map(locals())

    def get_geometry(self, geom):
        return OrderedDict((
            ('type', geom.geom_type),
            ('coordinates', geom.coords),
        ))

    def get_properties(self, instance):
        parent = self.parent
        fields = parent.fields

        # Filter fields to just those appropriate to use as GeoJSON
        # properties.
        property_fields = (
            (name, field) for (name, field) in fields.items()
            if (name != self.field_name and not field.write_only)
        )

        properties = OrderedDict()

        for name, field in property_fields:
            value = field.get_attribute(instance)
            value = field.to_representation(value)
            properties[name] = value

        return properties
