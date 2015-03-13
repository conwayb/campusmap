import os
import pkg_resources
import shutil
import sys
import time
from collections import OrderedDict
from urllib.request import urlretrieve

from decorator import decorator

from invoke import ctask as task, Collection

from arcutils.colorize import colorizer, printer


@decorator
def timed(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    elapsed_time = time.time() - start_time
    m, s = divmod(elapsed_time, 60)
    m = int(m)
    printer.info('\nElapsed time for {func.__name__}: {m:d}m {s:.4f}s\n'.format(func, **locals()))
    return result


@task
def env(ctx, name, user=None, host=None, project_name=None):
    """Configure based on environment."""
    config = ns.configuration()

    if user is None:
        user = config.get('user', os.environ['USER'])

    if host is None:
        host = config.get('host', 'hrimfaxi.oit.pdx.edu')

    if project_name is None:
        project_name = config.get('project_name')
        if project_name is None:
            dist = next(pkg_resources.find_distributions('.', only=True), None)
            assert dist is not None, (
                "Could not guess project name; build the project with pip before running tasks. "
                "You can also do `ns.configure({'project_name': '<project name>'})` in the "
                "project's tasks module or use the --project-name option."
                .format(name=name)
            )
            project_name = dist.project_name

    local_settings_file = 'local.{env}.cfg'.format(env=name)
    if not os.path.exists(local_settings_file):
        local_settings_file = 'local.cfg'

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings'.format(**locals()))
    os.environ.setdefault('LOCAL_SETTINGS_FILE', local_settings_file)
    from django.conf import settings

    env_dict = OrderedDict((
        ('env', name),
        ('project_name', project_name),
        ('user', user),
        ('host', host),
        ('local_settings_file', local_settings_file),
        ('ssh_cxn_str', '{user}@{host}'),
        ('base_path', '/vol/www/research/dev/{project_name}'),
        ('env_path', '{base_path}/{env}'),
        ('code_path', '{env_path}'),
        ('static_path', '{env_path}/static'),
        ('templates_path', '{env_path}/{project_name}/templates'),
        ('wsgi_file', '{env_path}/{project_name}/wsgi.py'),
        ('domain_name', settings.DOMAIN_NAME),
        ('static_root', settings.STATIC_ROOT),
    ))

    for k in env_dict:
        v = env_dict[k]
        env_dict[k] = v.format(**env_dict)

    ns.configure(env_dict)


def make_env_task(name):
    def func(ctx, user=None, host=None, project_name=None):
        env(ctx, name, user, host, project_name)
    func.__name__ = name
    func.__doc__ = 'Configure for {name} environment'.format(name=name)
    return task(func)

# These let us do `invoke dev ...` instead of `invoke env dev`
dev = make_env_task('dev')
stage = make_env_task('stage')
prod = make_env_task('prod')


@task(default=True)
def print_env(ctx):
    config = ns.configuration()
    printer.header('Environment ({env}):\n'.format(**config))
    for k, v in sorted(config.items()):
        print('    {k}: {v!r}'.format(**locals()))


@task
def manage(ctx, args):
    ctx.run('{exe} manage.py {args}'.format(exe=sys.executable, args=args))


@task
@timed
def build_static(ctx):
    manage(
        ctx,
        'collectstatic --noinput '
        '--ignore grunt --ignore less '  # bootstrap junk
        '--ignore r.js '
        '--ignore apidoc --ignore=closure-library --ignore=examples '  # openlayers junk
    )


@task(build_static)
@timed
def push_static(ctx, dry_run=False, delete=False, no_rm_static_dir=False):
    rsync(ctx, '{static_root}/', '{static_path}', dry_run, delete)
    if not no_rm_static_dir:
        config = ns.configuration()
        shutil.rmtree(config['static_root'])


@task
@timed
def push_templates(ctx, dry_run=False, delete=False):
    rsync(ctx, '{project_name}/templates/', '{templates_path}', dry_run, delete)
    rsync(ctx, '{project_name}/*/templates/', '{templates_path}', dry_run, delete)


@task
@timed
def push_code(ctx, dry_run=False, delete=False):
    rsync(ctx, './', '{code_path}', dry_run, delete, (
        '/.env',
        '/.env*/',
        '/.idea/',
        '/*.egg-info/',
        '/dist/',
        '/local.cfg',
        '/media/',
        '/static/',
        '/*/static/vendor/',
        'wsgi.py',
    ))


@task
@timed
def push_deps(ctx, dry_run=False, delete=True):
    rsync(
        ctx, '.env/src/', '{env_path}/.env/src', dry_run, delete,
        exclude_patterns=['*.egg-info/', '.env/', '.env*/', '.idea/', '/*/*/static/vendor/'])


@task
@timed
def install(ctx):
    remote(ctx, 'make install && make clean')


@task
@timed
def migrate(ctx):
    remote(ctx, 'make migrate')


@task
@timed
def restart(ctx):
    config = ns.configuration()
    scp(ctx, '{project_name}/wsgi.py', '{wsgi_file}')
    remote(ctx, 'touch {wsgi_file}')
    print('GETting {domain_name}...'.format(**config))
    urlretrieve('http://{domain_name}/'.format(**config), os.devnull)


@task
@timed
def deploy(ctx, dry_run=False, delete=False, no_deps=False, no_static=False, no_rm_static_dir=False,
           no_install=False, migrate=False):
    try:
        print_env(ctx)
        config = ns.configuration()
        print()
        print('Please review the configuration above.\n')
        if not migrate:
            print('NOTE: Migrations are not run by default; pass --migrate to run them.\n')
        prompt = colorizer.warning('Continue with deployment to {env}? [y/N] '.format(**config))
        answer = input(prompt)
        answer = answer.strip().lower()
        if answer in ('y', 'yes'):
            if not no_static:
                build_static(ctx)
            if not no_deps:
                push_deps(ctx, dry_run, delete)
            push_code(ctx, dry_run, delete)
            if not no_install:
                install(ctx)
            if migrate:
                migrate(ctx)
            if not no_static:
                push_static(ctx, dry_run, delete, no_rm_static_dir)
            restart(ctx)
    except KeyboardInterrupt:
        printer.error('\nAborted')


# Utilities

@task
def remote(ctx, cmd, where='{env_path}', path=None):
    """Run a command on the remote host.

    The directory ``where`` is changed into before the command is run.
    By default, this will be the env directory.

    """
    config = ns.configuration()
    cmd = cmd.format(**config)
    if path is not None:
        cmd = 'export PATH="$PATH:{path}" && {cmd}'.format(path=path, cmd=cmd)
    where = where.format(**config)
    cmd = 'ssh {ssh_cxn_str} "cd {where} && {cmd}"'.format(cmd=cmd, where=where, **config)
    ctx.run(cmd)


@task
def scp(ctx, local_path, remote_path):
    config = ns.configuration()
    local_path = local_path.format(**config)
    remote_path = remote_path.format(**config)
    ctx.run(
        'scp {local_path} {ssh_cxn_str}:{remote_path}'
        .format(local_path=local_path, remote_path=remote_path, **config))


@task
def rsync(ctx, local_path, remote_path, dry_run=False, delete=False, exclude_patterns=()):
    config = ns.configuration()
    local_path = local_path.format(**config)
    remote_path = remote_path.format(**config)
    dry_run = '--dry-run' if dry_run else ''
    delete = '--delete' if delete else ''
    excludes = make_rsync_excludes(*exclude_patterns)
    cmd = [
        'rsync', '-rltvz',
        '{dry_run}', '{delete}',
        '--no-perms', '--no-group', '--chmod=ug=rwX,o-rwx',
        '{excludes}',
        '{local_path}', '{ssh_cxn_str}:{remote_path}',
    ]
    cmd = ' '.join(cmd)
    cmd = cmd.format(
        local_path=local_path, remote_path=remote_path, dry_run=dry_run, delete=delete,
        excludes=excludes, **config)
    ctx.run(cmd)


def make_rsync_excludes(*patterns, include_defaults=True):
    """Make a string of "--exclude '{EXCLUDE}' ..." for ``patterns``."""
    if include_defaults:
        patterns += (
            '*.pyc',
            '__pycache__/',
            '*.swp',
            '.DS_Store',
        )
    return ' '.join("--exclude '{p}'".format(p=p) for p in patterns)


ns = Collection.from_module(sys.modules[__name__])
ns.configure({
    'project_name': 'campusmap',
})
