"""
ElasticBox Confidential
Copyright (c) 2014 All Right Reserved, ElasticBox Inc.

NOTICE:  All information contained herein is, and remains the property
of ElasticBox. The intellectual and technical concepts contained herein are
proprietary and may be covered by U.S. and Foreign Patents, patents in process,
and are protected by trade secret or copyright law. Dissemination of this
information or reproduction of this material is strictly forbidden unless prior
written permission is obtained from ElasticBox
"""

import keyring

import ebcli


def initialize_parser(subparsers):
    parser = subparsers.add_parser('login', help='Log in to ElasticBox and get your Authentication token')

    parser.add_argument(
        '--no-keychain',
        action='store_true',
        help="Don't store the token into the keyring default store",
        default=False)

    parser.set_defaults(func=execute_command)


def execute_command(args, _unknown):
    if 'token' not in args or not args.token:
        args.token = raw_input('Authentication Token: ')

    if args.token:
        try:
            response = ebcli.AuthenticatedSession(args.url, args.token).get('/services/workspaces')
        except ebcli.UnauthorizedException:
            raise ebcli.AuthTokenException('Failed to validate the token: Invalid token.')
        except ebcli.ApiException:
            raise ebcli.AuthTokenException('Failed to validate the token: Invalid url.')

        version = response.headers.get(ebcli.ELASTICBOX_RELEASE_HEADER, ebcli.ELASTICBOX_RELEASE)
        if not version.startswith(ebcli.ELASTICBOX_RELEASE):
            raise ebcli.AuthTokenException('Incompatible CLI version: API version: {0}'.format(version))

        if not args.no_keychain:
            credentials = '{0},{1}'.format(args.token, args.url)
            keyring.set_password(ebcli.ELASTICBOX_CREDENTIALS_NAME,
                                 ebcli.ELASTICBOX_CREDENTIALS_ACCOUNT,
                                 credentials)

        print 'Login Successfully'
    else:
        raise ebcli.AuthTokenException(
            'Failed to validate the token: Manage token from the profile drop-down menu.')
