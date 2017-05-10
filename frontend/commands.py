#!/usr/bin/env python3.5
import subprocess
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

from runcommands import command
from runcommands.commands import local, remote, show_config
from runcommands.util import abort, args_to_str, confirm, printer


@command(default_env='stage')
def deploy(config,
           host='hrimfaxi.oit.pdx.edu',
           build_dir='{remote.build.dir}',
           link_path='{remote.path.env}',
           dry_run=False, echo=False, hide=None):
    host = host.format(**config)
    build_dir = build_dir.format(**config)
    link_path = link_path.format(**config)

    printer.info('\n'.join((
        'Version: {config.version}',
        'Env: {config.env}',
        'Host: {host}',
        'Build directory: {build_dir}',
        'Link to build directory: {link_path}'
    )).format_map(locals()))

    if not dry_run:
        prompt = 'Continue with deployment of version {config.version} to {config.env} on {host}?'
        prompt = prompt.format_map(locals())
        confirm(config, prompt, yes_values=['yes'], abort_on_unconfirmed=True)

    build(config)

    cmd = args_to_str((
        'rsync', '-rltz',
        '--rsync-path "sudo -u {config.service.user} rsync"',
        "--exclude '.*'",
        "--exclude 'node_modules/'",
        "--exclude 'scripts/'",
        './', '{host}:{build_dir}'.format_map(locals()),
    ), format_kwargs=locals())
    if dry_run:
        printer.debug('[DRY RUN]', cmd)
    else:
        local(config, cmd, echo=echo, hide=hide)

    cmd = 'ln -sfn {build_dir} {link_path}'.format_map(locals())
    if dry_run:
        printer.debug('[DRY RUN]', cmd)
    else:
        remote(config, cmd, host, run_as='{service.user}', echo=echo, hide=hide)

    cmd = 'chmod -R u=rwX,g=rwX,o=rX {build_dir}'.format_map(locals())
    if dry_run:
        printer.debug('[DRY RUN]', cmd)
    else:
        remote(config, cmd, host, run_as='{service.user}', hide=hide)


@command
def build(config):
    build_css(config)
    build_js(config)


@command
def build_css(config):
    local(config, 'make css')


@command
def build_js(config):
    local(config, 'make js')


@command
def dev_server(config, host='0.0.0.0', port=3000):
    css_watcher = subprocess.Popen(['watch', 'make css', 'campusmap'])
    js_watcher = subprocess.Popen(['watch', 'make js', 'campusmap'])

    try:
        with TCPServer((host, port), SimpleHTTPRequestHandler) as http_server:
            printer.info('Serving . at {host}:{port}'.format_map(locals()))
            http_server.serve_forever()
    except Exception:
        printer.error('Could not run dev server; aborting...')
    except KeyboardInterrupt:
        printer.info('\nShutting down dev server...')

    css_watcher.terminate()
    js_watcher.terminate()
    css_watcher.wait()
    js_watcher.wait()
