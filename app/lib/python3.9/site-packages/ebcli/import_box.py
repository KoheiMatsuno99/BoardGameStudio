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
from ebcli import WORKSPACE_ID_ARG, BOXES_PATH_ARG, COMMENT_ARG, IMAGE_ARG, add_standard_argument


def initialize_parser(subparsers):
    parser = subparsers.add_parser('import', help='Import Box into a Workspace')

    add_standard_argument(parser, BOXES_PATH_ARG)
    add_standard_argument(parser, WORKSPACE_ID_ARG)
    add_standard_argument(parser, COMMENT_ARG)
    add_standard_argument(parser, IMAGE_ARG)
    parser.add_argument(dest='box_name', metavar='box-name', help='Box ID')
    parser.add_argument('--as-draft', dest='as_draft', action='store_true', default=False,
                        help='Push to the draft instead of creating a new version')
    parser.set_defaults(func=execute_command)


def execute_command(args, _unknown):
    session = AuthenticatedSession(args.url, args.token)

    boxes = Boxes(args.boxes_path, session)
    boxes.import_box(args.box_name, args.comment, args.workspace_id, args.image, as_draft=args.as_draft)
