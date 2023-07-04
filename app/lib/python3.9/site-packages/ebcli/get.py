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

import ebcli


def initialize_parser(subparsers):
    parser = subparsers.add_parser('get', help='Return specified object')

    ebcli.add_standard_argument(parser, ebcli.FIELDS_ARG)

    group = parser.add_mutually_exclusive_group(required=True)
    ebcli.add_standard_argument(group, ebcli.BOX_ID_ARG)
    ebcli.add_standard_argument(group, ebcli.INSTANCE_ID_ARG)
    ebcli.add_standard_argument(group, ebcli.WORKSPACE_ID_ARG)

    parser.set_defaults(func=execute_command)


def execute_command(args, _unknown):
    session = ebcli.AuthenticatedSession(args.url, args.token)
    formatter = ebcli.Formatter(args)

    if args.box_id:
        response = session.get('/services/boxes/{0}', args.box_id)
        formatter.write(response, prefix='BOX', fields=ebcli.DEFAULT_BOX_FIELDS)

    if args.instance_id:
        response = session.get('/services/instances/{0}', args.instance_id).json()
        formatter.write(response, prefix='INSTANCE', fields=ebcli.DEFAULT_INSTANCE_FIELDS)

    if args.workspace_id:
        response = session.get('/services/workspaces/{0}', args.workspace_id).json()
        formatter.write(response, prefix='WORKSPACE', fields=ebcli.DEFAULT_WORKSPACE_FIELDS)
