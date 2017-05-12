#!/usr/bin/env python3.6
import os

from runcommands import command
from runcommands.commands import local, remote, show_config
from runcommands.util import confirm, printer


@command(default_env='stage')
def deploy(config,
           user='{service.user}',
           host='{deploy.host}',
           local_build_dir='{local.build.root}',
           remote_build_dir='{deploy.build.dir}',
           link_path='{deploy.path.link}',
           dry_run=False, echo=False, hide=None):

    user = user.format(**config)
    host = host.format(**config)
    local_build_dir = local_build_dir.format(**config)
    remote_build_dir = remote_build_dir.format(**config)
    link_path = link_path.format(**config)

    rsync_local_path = os.path.join(local_build_dir, '')
    rsync_remote_path = f'{host}:{remote_build_dir}'

    def run_local_cmd(*args):
        if dry_run:
            printer.debug('[DRY RUN]', ' '.join(args))
        else:
            local(config, args, echo=echo, hide=hide)

    def run_remote_command(*args):
        if dry_run:
            printer.debug('[DRY RUN]', ' '.join(args))
        else:
            remote(config, args, host, run_as=user, echo=echo, hide=hide)

    printer.info(
        f'Env: {config.env}',
        f'Version: {config.version}',
        f'Host: {host}',
        f'Local build directory: {local_build_dir}',
        f'Remote build directory: {remote_build_dir}',
        f'Link to build directory: {link_path}',
        sep='\n')

    if not dry_run:
        prompt = f'Continue with deployment of version {config.version} to {config.env} on {host}?'
        confirm(config, prompt, yes_values=['yes'], abort_on_unconfirmed=True)

    printer.hr(color='header')
    printer.header('LOCAL')
    printer.hr(color='header')

    printer.header('Building...')
    run_local_cmd(
        'ng', 'build',
        '--environment', config.env,
        '--target', 'production',
        '--output-path', local_build_dir,
    )

    printer.hr(color='header')
    printer.header('REMOTE')
    printer.hr(color='header')

    printer.header('Provisioning...')
    run_remote_command(f'mkdir -p {remote_build_dir}')

    printer.header('Pushing...')
    run_local_cmd(
        'rsync', '-rltz',
        f'--rsync-path "sudo -u {user} rsync"',
        '--dry-run' if dry_run else '',
        rsync_local_path, rsync_remote_path,
    )

    printer.header('Linking...')
    run_remote_command(f'ln -sfn {remote_build_dir} {link_path}')

    printer.header('Setting permissions...')
    run_remote_command(f'chmod -R u=rwX,g=rwX,o=rX {remote_build_dir}')
