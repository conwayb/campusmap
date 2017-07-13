import os
from importlib import import_module

from runcommands import command
from runcommands.util import abort, printer

from arctasks.commands import *
from arctasks.django import setup as django_setup


@command(env='dev', timed=True)
def init(config, overwrite=False, drop_db=False):
    virtualenv(config, overwrite=overwrite)
    install(config)
    createdb(config, drop=drop_db)
    migrate(config)


@command(default_env='dev', timed=True)
def import_gis_data(config, source_dir='../gisdata', app=None, model=None, overwrite=False,
                    verbose=False, quiet=False, dry_run=False):
    django_setup(config)

    from django.apps import apps
    from django.utils.module_loading import module_has_submodule
    from campusmap.importer import Importer

    args = (source_dir,)
    kwargs = dict(overwrite=overwrite, verbose=verbose, quiet=quiet, dry_run=dry_run)

    importers = []

    if model and '.' in model:
        if app:
            raise ValueError('You passed `app` via `--app` and via `--model`')
        app, model = model.split('.')

    if app:
        try:
            app_config = apps.get_app_config(app)
        except LookupError as exc:
            abort(1, str(exc))
        app_configs = [app_config]
    else:
        app_configs = apps.get_app_configs()

    app_configs = [c for c in app_configs if module_has_submodule(c.module, 'importer')]

    for app_config in app_configs:
        importer_module = import_module(f'{app_config.name}.importer')
        objects = vars(importer_module).values()
        importers.extend(
            obj for obj in objects if (
                isinstance(obj, type) and
                issubclass(obj, Importer) and
                (not obj.abstract)
            )
        )

    if model:
        model = apps.get_model(app, model)
        importers = [importer for importer in importers if importer.model is model]

    if not importers:
        printer.warning('No importers found')

    importers = sorted(importers, key=lambda importer: importer.__name__)

    for importer_class in importers:
        importer = importer_class(*args, **kwargs)
        importer.run()


# TEMPORARY -----------------------------------------------------------


@command(default_env='stage')
def make_mod_wsgi_config(config, restart=True):
    mod_wsgi(config, 'stop')
    remote(config, 'mkdir -p {mod_wsgi.site}')
    remote(config, (
        '/usr/bin/mod_wsgi-express', 'setup-server',
        '--server-root', '{mod_wsgi.site}',
        '--server-name', '{mod_wsgi.server_name}',
        '--server-alias', '{mod_wsgi.server_alias}',
        '--user', '{service.user}',
        '--group', '{service.group}',
        '--port', '{mod_wsgi.port}',
        '--processes', '{mod_wsgi.processes}',
        '--threads', '{mod_wsgi.threads}',
        '--entry-point', '{remote.path.wsgi_file}',
        '--document-root', '{remote.path.front_end.static}',
        '--directory-index', 'index.html',
        '--url-alias', '/api/static {remote.path.static}',
    ), sudo=True)
    if restart:
        mod_wsgi(config, 'start')


@command(default_env='stage')
def mod_wsgi(config, action):
    if action == 'log':
        remote(config, 'tail -f {mod_wsgi.site}/error_log', sudo=True)
    else:
        remote(config, ('{mod_wsgi.apachectl}', action), sudo=True)
