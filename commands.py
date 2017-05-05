from runcommands import command

from arctasks.commands import *


@command(env='dev', timed=True)
def init(config, overwrite=False, drop_db=False):
    virtualenv(config, overwrite=overwrite)
    install(config)
    npm_install(config, where='{package}:static', modules=[])
    createdb(config, drop=drop_db)
    migrate(config)
    sass(config)
    test(config, force_env='test')
