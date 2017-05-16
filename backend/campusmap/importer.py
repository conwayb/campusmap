import abc
import os

from django.contrib.gis.utils import LayerMapping as BaseLayerMapping

from arcutils.colorize import printer
from arcutils.decorators import cached_property


class LayerMapping(BaseLayerMapping):

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


class GeoJSONImporter(metaclass=abc.ABCMeta):

    def __init__(self, path, from_srid=4326, overwrite=False, verbose=False, quiet=False,
                 dry_run=False):
        path = self.normalize_path(path)
        if os.path.isdir(path):
            path = os.path.join(path, self.default_file_name)

        self.path = path
        self.from_srid = from_srid
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

    @cached_property
    def default_file_name(self):
        return f'{self.model_name_plural}.geojson'

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
            self.warning(f'Removing {self.model_name_plural}...')
            if self.real_run:
                self.model.objects.all().delete()
            printer.print('Done')

        self.print(f'Importing {self.model_name_plural}...')
        if self.real_run:
            args = {
                'source_srs': self.from_srid,
                'transform': self.from_srid != 4326,
            }
            importer = LayerMapping(self.model, self.path, self.field_name_map, **args)
            importer.save(strict=True, silent=self.quiet, verbose=self.verbose)

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
        printer.print(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.print('WARNING:', *args, color='warning', **kwargs)
