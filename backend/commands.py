from runcommands import command

from arctasks.commands import *
from arctasks.django import setup as django_setup


@command(env='dev', timed=True)
def init(config, overwrite=False, drop_db=False):
    virtualenv(config, overwrite=overwrite)
    install(config)
    createdb(config, drop=drop_db)
    migrate(config)


@command(default_env='dev', timed=True)
def import_geojson(config, source_dir='../gisdata', overwrite=False, verbose=False, quiet=False,
                   dry_run=False):
    django_setup(config)
    from campusmap.buildings.importer import BuildingsImporter

    importer = BuildingsImporter(
        source_dir, overwrite=overwrite, verbose=verbose, quiet=quiet, dry_run=dry_run)
    importer.run()
