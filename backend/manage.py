#!/usr/bin/env python
import argparse
import os
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False, usage=argparse.SUPPRESS)
    parser.add_argument('--env', default=None)
    args, remaining_args = parser.parse_known_args()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusmap.settings')
    os.environ.setdefault('LOCAL_SETTINGS_CONFIG_QUIET', 'true')

    if args.env:
        local_settings_file = 'local.{args.env}.cfg'.format(args=args)
        os.environ['LOCAL_SETTINGS_FILE'] = local_settings_file

    from django.core.management import execute_from_command_line
    execute_from_command_line([sys.argv[0]] + remaining_args)
