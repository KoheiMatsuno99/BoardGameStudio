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

import ebcli


def initialize_parser(subparsers):
    parser = subparsers.add_parser('workspaces', help='List workspaces')

    ebcli.add_standard_argument(parser, ebcli.FIELDS_ARG, default=ebcli.DEFAULT_WORKSPACE_FIELDS)
    parser.set_defaults(func=execute_command)


def execute_command(args, _unknown):
    session = ebcli.AuthenticatedSession(args.url, args.token)
    workspaces = session.get('/services/workspaces').json()

    formatter = ebcli.Formatter(args)
    formatter.write(workspaces, prefix='WORKSPACE', fields=args.fields)
