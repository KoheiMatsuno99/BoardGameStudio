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

INSTANCE_DEFAULT_FIELDS = ['id', 'name', 'state', 'owner', 'tags']


def initialize_parser(subparsers):
    parser = subparsers.add_parser('instances', help='List instances')

    ebcli.add_standard_argument(parser, ebcli.FIELDS_ARG, default=INSTANCE_DEFAULT_FIELDS)
    ebcli.add_standard_argument(parser, ebcli.TAGS_ARG)
    ebcli.add_standard_argument(parser, ebcli.WORKSPACE_ID_ARG)

    parser.set_defaults(func=execute_command)


def execute_command(args, _unknown):
    session = ebcli.AuthenticatedSession(args.url, args.token)

    instances = list_instances(session, args.workspace_id, args.tags)

    formatter = ebcli.Formatter(args)
    formatter.write(instances)


def list_instances(session, workspace_id=None, tags=None):
    if workspace_id:
        instances = session.get('/services/workspaces/{0}/instances', workspace_id).json()
    else:
        profile = session.get('/services/profile').json()
        instances = session.get('/services/workspaces/{0}/instances', profile['workspace']).json()

    if tags:
        filtered = []

        for instance in instances:
            if 'tags' in instance:
                if set(instance['tags']).issuperset(tags.split(',')):
                    filtered.append(instance)

        instances = filtered

    return instances
