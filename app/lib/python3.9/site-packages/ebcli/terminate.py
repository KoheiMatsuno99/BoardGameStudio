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

import httplib
import ebcli


def initialize_parser(subparsers):
    parser = subparsers.add_parser('terminate', help='Terminate the given instance')

    ebcli.add_standard_argument(parser, ebcli.INSTANCE_ID_ARG, required=True)
    parser.set_defaults(func=execute_command)


def execute_command(args, _unknown):
    session = ebcli.AuthenticatedSession(args.url, args.token)
    instance = get(session, args.instance_id)
    if instance['state'] != 'done':
        session.delete('/services/instances/{0}?operation=force_terminate', args.instance_id)
    else:
        session.delete('/services/instances/{0}?operation=terminate', args.instance_id)


def get(session, instance_id):
    response = session.get('/services/instances/{0}'.format(instance_id))

    _check_status_code(response)
    return response.json()


def _check_status_code(response, status_code=httplib.OK):
    assert response.status_code == status_code, 'Received an unexpected status code: {0}. Response: {1}'.format(
        response.status_code, response.text)
