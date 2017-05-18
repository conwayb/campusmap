import abc
import glob
import os

from django.contrib.gis.utils import LayerMapping as BaseLayerMapping

from arcutils.colorize import printer
from arcutils.decorators import cached_property


class Importer(metaclass=abc.ABCMeta):

    abstract = True
    filters = ()
    source_srid = 4326

    def __init__(self, path, filters=None, source_srid=None, overwrite=False, verbose=False,
                 quiet=False, dry_run=False):
        path = self.normalize_path(path)
        if os.path.isdir(path):
            path = self.get_path_from_dir(path)

        self.path = path

        if filters is not None:
            self.filters = filters

        if source_srid is not None:
            self.source_srid = source_srid

        self.overwrite = overwrite
        self.verbose = verbose
        self.quiet = quiet
        self.dry_run = dry_run
        self.real_run = not dry_run

    @property
    @abc.abstractmethod
    def model(self):
        raise NotImplementedError('Set `model` on subclass')

    @property
    @abc.abstractmethod
    def field_name_map(self):
        raise NotImplementedError('Set `field_name_map` on subclass')

    @abc.abstractmethod
    def get_path_from_dir(self, path):
        raise NotImplementedError('Implement `get_path_from_dir` in subclass')

    @cached_property
    def model_name(self):
        return self.model._meta.verbose_name

    @cached_property
    def model_name_plural(self):
        return self.model._meta.verbose_name_plural

    def pre_run(self):
        pass

    def run(self):
        self.pre_run()

        if self.overwrite:
            self.warning(f'Removing {self.model_name_plural}...', end=' ')
            if self.real_run:
                self.model.objects.all().delete()
            printer.warning('Done')

        self.print(f'Importing {self.model_name_plural}...', end=' ')
        if self.real_run:
            args = {
                'source_srs': self.source_srid,
                'transform': self.source_srid != 4326,
                'filters': self.filters,
            }
            importer = LayerMapping(self.model, self.path, self.field_name_map, **args)
            importer.save(strict=True, silent=self.quiet, verbose=self.verbose)
        printer.print('Done')

        self.post_run()

    def post_run(self):
        pass

    def normalize_path(self, path):
        return os.path.normpath(os.path.abspath(os.path.expanduser(path)))

    def print(self, *args, **kwargs):
        if self.quiet:
            return
        if self.dry_run:
            args = ('[DRY RUN]',) + args
        printer.print(*args, flush=True, **kwargs)

    def warning(self, *args, **kwargs):
        self.print('WARNING:', *args, color='warning', **kwargs)


class GeoJSONImporter(Importer):

    importer_type = 'geojson'

    def get_path_from_dir(self, path):
        base_name = self.model_name_plural.replace(' ', '-')
        geojson_path = os.path.join(path, f'{base_name}.geojson')
        if not os.path.isfile(geojson_path):
            raise FileNotFoundError(
                f'No GeoJSON file found at "{path}"; tried "{geojson_path}"')
        return geojson_path


class ShapefileImporter(Importer):

    importer_type = 'shapefile'

    def get_path_from_dir(self, path):
        base_name = self.model_name_plural.replace(' ', '-')
        shapefile_path = os.path.join(path, base_name, f'{base_name}.shp')

        # Exact match
        if os.path.isfile(shapefile_path):
            return shapefile_path

        # Fuzzy match of *.shp
        glob_shapefile_path = os.path.join(path, base_name, '*.shp')
        candidates = glob.glob(glob_shapefile_path)

        if len(candidates) == 1:
            shapefile_path = candidates[0]
            return shapefile_path

        raise FileNotFoundError(
            f'No Shapefile found at "{path}"; tried "{shapefile_path}" and {glob_shapefile_path}')


class RLISShapefileImporter(ShapefileImporter):

    importer_type = 'rlis-shapefile'
    source_srid = 2913


# Utilities -----------------------------------------------------------


class LayerMapping(BaseLayerMapping):

    # Allows features to be filtered.
    # Trims leading and trailing whitespace from property values.
    # Converts empty strings to NULL for nullable fields.

    def __init__(self, *args, layer=0, filters=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.layer_index = layer
        self.filters = filters
        self._layer = self.layer
        del self.layer

    @cached_property
    def layer(self):
        return LayerWrapper(self, self._layer, self.filters)

    def feature_kwargs(self, feature):
        kwargs = super().feature_kwargs(feature)
        for model_field_name in kwargs:
            value = kwargs[model_field_name]
            if isinstance(value, str):
                value = value.strip()
                field = self.model._meta.get_field(model_field_name)
                if not value and field.null:
                    value = None
                kwargs[model_field_name] = value
        return kwargs


class LayerWrapper:

    def __init__(self, mapping, layer, filters):
        self.__mapping = mapping
        self.__layer = layer
        self.__filters = filters

    def __iter__(self):
        return (feature for feature in self.__layer if self.__include(feature))

    def __getattr__(self, name):
        return getattr(self.__layer, name)

    def __include(self, feature):
        data = self.__mapping.feature_kwargs(feature)
        return all(f(data) for f in self.__filters)
