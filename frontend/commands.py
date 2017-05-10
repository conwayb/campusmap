import subprocess
#!/usr/bin/env python3.6
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

    printer.info(
        f'Version: {config.version}',
        f'Env: {config.env}',
        f'Host: {host}',
        f'Build directory: {build_dir}',
        f'Link to build directory: {link_path}',
        sep='\n')

    if not dry_run:
        prompt = f'Continue with deployment of version {config.version} to {config.env} on {host}?'
        confirm(config, prompt, yes_values=['yes'], abort_on_unconfirmed=True)

    build(config)

    cmd = (
        'rsync', '-rltz',
        f'--rsync-path "sudo -u {config.service.user} rsync"',
        "--exclude '.*'", "--exclude 'node_modules/'",
        './', f'{host}:{build_dir}',
    )
    if dry_run:
        printer.debug('[DRY RUN]', cmd)
    else:
        local(config, cmd, echo=echo, hide=hide)

    cmd = f'ln -sfn {build_dir} {link_path}'
    if dry_run:
        printer.debug('[DRY RUN]', cmd)
    else:
        remote(config, cmd, host, run_as='{service.user}', echo=echo, hide=hide)

    cmd = f'chmod -R u=rwX,g=rwX,o=rX {build_dir}'
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
            printer.info(f'Serving . at {host}:{port}')
            http_server.serve_forever()
    except Exception:
        printer.error('Could not run dev server; aborting...')
    except KeyboardInterrupt:
        printer.info('\nShutting down dev server...')

    css_watcher.terminate()
    js_watcher.terminate()
    css_watcher.wait()
    js_watcher.wait()
