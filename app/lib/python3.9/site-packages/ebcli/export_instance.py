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

from ebcli import Boxes, AuthenticatedSession
from ebcli import BOXES_PATH_ARG, add_standard_argument


def initialize_parser(subparsers):
    parser = subparsers.add_parser('export-instance', help='Export Instace boxes to a folder')

    add_standard_argument(parser, BOXES_PATH_ARG)
    parser.add_argument(dest='instance_id', metavar='instance-id', help='ID of the Instance to export')
    parser.set_defaults(func=execute_command)


def execute_command(args, _unknown):
    session = AuthenticatedSession(args.url, args.token)
    Boxes(args.boxes_path, session).export_instance_boxes(args.instance_id)
