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

import sys
import yaml

import ebcli


def initialize_parser(subparsers):
    parser = subparsers.add_parser('deploy', help='Deploy application from document')

    ebcli.add_standard_argument(parser, ebcli.WORKSPACE_ID_ARG)
    ebcli.add_standard_argument(parser, ebcli.TAGS_ARG)
    ebcli.add_standard_argument(parser, ebcli.CLAIMS_ARG)
    parser.add_argument(dest='input', help='Application document to publish')
    parser.set_defaults(func=execute_command)


def execute_command(args, _unknown):
    session = ebcli.AuthenticatedSession(args.url, args.token)
    if 'workspace_id' in args and args.workspace_id:
        workspace = args.workspace_id
    else:
        profile = session.get('/services/profile').json()
        workspace = profile['workspace']

    boxes = session.get('/services/workspaces/{0}/boxes', workspace).json()
    boxes = boxes + session.get('/services/boxes', workspace).json()

    tags = args.tags if 'tags' in args and args.tags else []
    claims = args.claims if 'claims' in args and args.claims else []
    _deploy_boxes(args, boxes, session, claims, workspace, tags)


def _deploy_boxes(args, boxes, session, claims, workspace, tags):
    stacks = {}
    for instance_name, spec in _load_application(args).iteritems():
        box = _lookup_box(spec, boxes)
        box_stack = _get_box_stack(box, session, stacks)

        policy = _lookup_policy_box(spec, boxes, claims)
        policy_stack = _get_policy_stack(policy, session, stacks)

        request = {
            'schema': 'http://elasticbox.net/schemas/deploy-instance-request',
            'name': instance_name,
            'owner': workspace,
            'box': {
                'id': box['id'],
                'variables': _prepare_variables(box_stack, box['id'], spec, tags)
            },
            'policy_box': {
                'id': policy['id'],
                'variables': _prepare_variables(policy_stack, policy['id'], spec, tags)
            },
            'instance_tags': tags + spec['tags'] if 'tags' in spec else tags
        }
        _post_deploy_request(args, session, request)


def _post_deploy_request(args, session, request):
    formatter = ebcli.Formatter(args)
    response = session.post('/services/instances', json=request).json()
    formatter.write(response, prefix='INSTANCE', fields=ebcli.DEFAULT_INSTANCE_FIELDS)


def _get_box_stack(box, session, stacks):
    box_id = box['id']

    if box_id not in stacks:
        box_stack = session.get('/services/boxes/{0}/stack', box_id).json()
        stacks[box_id] = box_stack
    else:
        box_stack = stacks[box_id]

    return box_stack


def _get_policy_stack(policy, session, stacks):
    policy_id = policy['id']

    if policy_id not in stacks:
        policy_stack = session.get('/services/boxes/{0}/stack', policy_id).json()
        stacks[policy_id] = policy_stack
    else:
        policy_stack = stacks[policy_id]

    return policy_stack


def _find_box_in_stack(box_id, stack):
    child_box = next((box for box in stack if box['id'] == box_id), None)
    if not child_box:
        # Some boxes are pointing to unversioned boxes and the stack is giving only versioned boxes.
        # This is a fallback.
        child_box = next((box for box in stack if 'version' in box and box['version']['box'] == box_id), None)
    return child_box


def _load_application(args):
    if args.input is not None:
        with open(args.input, 'r') as document:
            contents = document.read().decode('utf-8')
    else:
        contents = sys.stdin.read().decode('utf-8')

    return yaml.load(contents)


def _lookup_box_variable(stack, box_id, name, scope):
    box = _find_box_in_stack(box_id, stack)

    if not scope:
        for variable in box['variables']:
            if variable['name'] == name:
                return variable
    else:
        if 'variables' in box:
            for variable in box['variables']:
                if variable['name'] == scope[0] and variable['type'] == 'Box':
                    variable_found = _lookup_box_variable(stack, variable['value'], name, scope[1:])
                    if variable_found:
                        return variable_found


def _get_scope_and_name_from_specname(name):
    splitted_name = name.split('.')
    return splitted_name[:-1], splitted_name[-1]


def _lookup_box(spec, boxes):
    _, name = spec['box'].split('/')

    for box in boxes:
        if 'friendly_id' in box and box['friendly_id'] == name:
            return box

        if box['name'] == name:
            return box

    raise Exception('Box {0} not found.'.format(name))


def _lookup_policy_box(spec, boxes, claims):
    claims = spec['policy'] + claims

    for box in boxes:
        if 'claims' in box and set(claims).issubset(box['claims']):
            return box

    raise Exception('Box with claims {0} not found.'.format(', '.join(claims)))


def _prepare_variables(stack, box_id, spec, tags):
    variables = []

    for spec_name, variable_value in spec['variables'].iteritems():
        scope, name = _get_scope_and_name_from_specname(spec_name)
        variable = _lookup_box_variable(stack, box_id, name, scope)

        if variable:
            if variable['type'] == 'Binding':
                variable['tags'] = variable_value + tags
            else:
                variable['value'] = variable_value

            if scope:
                variable['scope'] = '.'.join(scope)

            variables.append(variable)

    return variables
