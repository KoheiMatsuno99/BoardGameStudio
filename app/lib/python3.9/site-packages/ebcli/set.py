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
    parser = subparsers.add_parser('set', help='Update a variable of the given box or instance')

    ebcli.add_standard_argument(parser, ebcli.VARIABLE_ARG)

    group = parser.add_mutually_exclusive_group(required=True)
    ebcli.add_standard_argument(group, ebcli.BOX_ID_ARG)
    ebcli.add_standard_argument(group, ebcli.INSTANCE_ID_ARG)

    parser.set_defaults(func=execute_command)


def execute_command(args, _unknown):
    session = ebcli.AuthenticatedSession(args.url, args.token)

    if args.box_id:
        box = _update_box_variable(session, args.box_id, args.variable[0], args.variable[1])

        formatter = ebcli.Formatter(args)
        formatter.write(box)

    if args.instance_id:
        raise NotImplementedError()


def _update_box_variable(session, box_id, name, value):
    box = session.get('/services/boxes/{0}', box_id).json()

    if '.' in name:
        scope, name = name.rsplit('.', 1)
    else:
        scope = None

    for variable in box['variables']:
        if name == variable['name']:
            if 'scope' in variable and scope != variable['scope']:
                break

            variable['value'] = value

    return session.put('/services/boxes/{0}', box_id, json=box).json()
