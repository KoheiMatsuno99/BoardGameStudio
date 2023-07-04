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
    parser = subparsers.add_parser('shutdown', help='Shutdown the given instance')

    ebcli.add_standard_argument(parser, ebcli.INSTANCE_ID_ARG, required=True)
    parser.set_defaults(func=execute_command)


def execute_command(args, _unknown):
    session = ebcli.AuthenticatedSession(args.url, args.token)
    session.put('/services/instances/{0}/shutdown', args.instance_id)
