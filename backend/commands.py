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
def start_mod_wsgi(config, server_name='{package}.staging.rc.pdx.edu', port=9007):
    remote(config, (
        '/usr/bin/mod_wsgi-express', 'start-server',
        '--server-name', server_name,
        '--server-alias', '{package}*',
        '--port', str(port),
        '--processes', '2',
        '--threads', '4',
        '--entry-point', '{remote.build.wsgi_file}',
    ), run_as='{service.user}', strategy='ssh-background')


from runcommands.runners.local import LocalRunner
from runcommands.runners.remote import RemoteRunner


class RemoteRunnerSSH(RemoteRunner):

    name = 'ssh-background'

    def run(self, cmd, host, user=None, cd=None, path=None, prepend_path=None,
            append_path=None, sudo=False, run_as=None, echo=False, hide=False, timeout=30,
            debug=False):
        ssh_connection_str = '{user}@{host}'.format(user=user, host=host) if user else host
        path = self.munge_path(path, prepend_path, append_path, '$PATH')
        cmd = f'nohup {cmd} &>/dev/null'
        remote_command = self.get_remote_command(cmd, user, cd, path, sudo, run_as)
        ssh_cmd = ['ssh', '-f', ssh_connection_str, remote_command]
        local_runner = LocalRunner()
        return local_runner.run(ssh_cmd, echo=echo, hide=hide, timeout=timeout, debug=debug)
