#!/usr/bin/env python
"""
ElasticBox Confidential
Copyright (c) 2015 All Right Reserved, ElasticBox Inc.

NOTICE:  All information contained herein is, and remains the property
of ElasticBox. The intellectual and technical concepts contained herein are
proprietary and may be covered by U.S. and Foreign Patents, patents in process,
and are protected by trade secret or copyright law. Dissemination of this
information or reproduction of this material is strictly forbidden unless prior
written permission is obtained from ElasticBox
"""

import argparse
import os
import sys
import logging
import keyring

import ebcli.boxes
import ebcli.build
import ebcli.delete
import ebcli.deploy
import ebcli.get
import ebcli.export
import ebcli.export_instance
import ebcli.import_box
import ebcli.instances
import ebcli.login
import ebcli.logout
import ebcli.poweron
import ebcli.reconfigure
import ebcli.reinstall
import ebcli.set
import ebcli.shutdown
import ebcli.terminate
import ebcli.workspaces

DEFAULT_ELASTICBOX_URL = os.getenv('ELASTICBOX_URL', 'https://cam.ctl.io')
DEFAULT_ELASTICBOX_TOKEN = os.getenv('ELASTICBOX_TOKEN', None)


def main():
    debug = False

    try:
        parser = argparse.ArgumentParser(
            description='ElasticBox commands',
            epilog="See 'ebcli command --help' for more information")

        parser.add_argument('--url', help='Host to connect', default=DEFAULT_ELASTICBOX_URL)
        parser.add_argument('--token', help='Authentication Token', default=DEFAULT_ELASTICBOX_TOKEN)
        parser.add_argument('--debug', action='store_true', default=False)
        parser.add_argument('--verbose', action='store_true', default=False)
        parser.add_argument('-j', '--json', action='store_true', default=False)

        credentials = keyring.get_password(ebcli.ELASTICBOX_CREDENTIALS_NAME,
                                           ebcli.ELASTICBOX_CREDENTIALS_ACCOUNT)
        if credentials:
            token, url = credentials.split(',')
            parser.set_defaults(token=token, url=url)
        else:
            token = None
            url = DEFAULT_ELASTICBOX_URL

        subparsers = parser.add_subparsers(title='Commands', dest='command')

        _initialize_commands(subparsers)

        args, unknown_args = parser.parse_known_args()

        if 'debug' in args and debug:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            root = logging.getLogger()
            root.addHandler(handler)
            root.setLevel(logging.DEBUG)
            handler.setLevel(logging.DEBUG)

        if not args.token:
            if args.command != 'login':
                raise ebcli.AuthTokenException('Need to authenticate before using the command line')
        else:
            # Reset token if the url is different that the one stored
            if args.command == 'login' and args.url != url and token and not args.token:
                args.token = None

        args.func(args, unknown_args)

    except ebcli.AuthTokenException, auth:
        print >> sys.stderr, ebcli.TermColors.FAIL.value + auth.message + ebcli.TermColors.ENDC.value
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)
    except ebcli.ApiException, api:
        logging.exception(api)
        print >> sys.stderr, ebcli.TermColors.FAIL.value + api.message + ebcli.TermColors.ENDC.value

        sys.exit(2)
    except Exception, ex:
        logging.exception(ex)
        print >> sys.stderr, ebcli.TermColors.FAIL.value + ex.message + ebcli.TermColors.ENDC.value

        sys.exit(1)

    sys.exit(0)


def _initialize_commands(subparsers):
    ebcli.boxes.initialize_parser(subparsers)
    ebcli.build.initialize_parser(subparsers)
    ebcli.delete.initialize_parser(subparsers)
    ebcli.deploy.initialize_parser(subparsers)
    ebcli.get.initialize_parser(subparsers)
    ebcli.export.initialize_parser(subparsers)
    ebcli.export_instance.initialize_parser(subparsers)
    ebcli.import_box.initialize_parser(subparsers)
    ebcli.instances.initialize_parser(subparsers)
    ebcli.login.initialize_parser(subparsers)
    ebcli.logout.initialize_parser(subparsers)
    ebcli.set.initialize_parser(subparsers)
    ebcli.poweron.initialize_parser(subparsers)
    ebcli.reconfigure.initialize_parser(subparsers)
    ebcli.reinstall.initialize_parser(subparsers)
    ebcli.shutdown.initialize_parser(subparsers)
    ebcli.terminate.initialize_parser(subparsers)
    ebcli.workspaces.initialize_parser(subparsers)


if __name__ == '__main__':
    main()
