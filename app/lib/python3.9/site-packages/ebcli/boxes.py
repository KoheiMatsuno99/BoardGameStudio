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


BOX_DEFAULT_FIELDS = ['id', 'name', 'owner', 'requirements']


def initialize_parser(subparsers):
    parser = subparsers.add_parser('boxes', help='List boxes')

    ebcli.add_standard_argument(parser, ebcli.FIELDS_ARG, default=BOX_DEFAULT_FIELDS)
    ebcli.add_standard_argument(parser, ebcli.REQUIREMENTS_ARG)
    ebcli.add_standard_argument(parser, ebcli.WORKSPACE_ID_ARG)

    parser.set_defaults(func=execute_command)


def execute_command(args, _unknown):
    session = ebcli.AuthenticatedSession(args.url, args.token)

    boxes = list_boxes(session, args.workspace_id, args.requirements)

    formatter = ebcli.Formatter(args)
    formatter.write(boxes, args.fields)


def list_boxes(session, workspace_id=None, requirements=None):
    if workspace_id:
        boxes = session.get('/services/workspaces/{0}/boxes', workspace_id).json()
    else:
        boxes = session.get('/services/boxes').json()

    if requirements:
        filtered = []

        for box in boxes:
            if 'requirements' in box:
                if set(box['requirements']).issuperset(requirements.split(',')):
                    filtered.append(box)

        boxes = filtered

    return boxes
