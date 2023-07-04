"""
ElasticBox Confidential
Copyright (c) 2012 All Right Reserved, ElasticBox Inc.

NOTICE:  All information contained herein is, and remains the property
of ElasticBox. The intellectual and technical concepts contained herein are
proprietary and may be covered by U.S. and Foreign Patents, patents in process,
and are protected by trade secret or copyright law. Dissemination of this
information or reproduction of this material is strictly forbidden unless prior
written permission is obtained from ElasticBox
"""

import argparse
import os
import tempfile
import subprocess
import sys

import ebcli
from ebcli import Boxes, AuthenticatedSession

from jinja2 import Environment, FileSystemLoader

EBX_AGENT_DIRECTORY = os.path.dirname(__file__)
EBX_TEMPORARY_FOLDER = '.elasticbox'
EBX_CONTAINER_PATH = '/opt/ebx'


def initialize_parser(subparsers):
    parser = subparsers.add_parser('build', help='Build container for the specified box')

    ebcli.add_standard_argument(parser, ebcli.IMAGE_ARG)
    ebcli.add_standard_argument(parser, ebcli.BOXES_PATH_ARG)
    parser.add_argument(dest='box_id')
    parser.add_argument('--dockerfile', type=argparse.FileType('w'), default=sys.stdout)

    parser.set_defaults(func=execute_command)


def execute_command(args, unknown_args):
    session = AuthenticatedSession(args.url, args.token)

    source = Boxes(args.boxes_path if 'boxes_path' in args else os.getcwd(), session)

    context = {
        'path': EBX_CONTAINER_PATH,
        'box': args.box_id,
        'image': args.image or 'ubuntu',
        'url': args.url
    }

    if 'dockerfile' in args and args.dockerfile:
        box_collection, scripts, ports = _get_setup_data(source, args.box_id)

        filename = os.path.abspath(args.dockerfile.name)

        context['boxes_path'] = os.path.relpath(os.path.dirname(filename), args.boxes_path)
        context['scripts'] = scripts
        context['ports'] = ports
        context['boxes'] = box_collection

        _generate_dockerfile(context, args.dockerfile)
    else:
        ebx_path = os.path.join(tempfile.gettempdir(), EBX_TEMPORARY_FOLDER)

        boxes = Boxes(os.path.join(ebx_path, 'boxes'), session)
        boxes.export_box(args.box_id, recursive=True, source=source)

        box_collection, scripts, ports = _get_setup_data(boxes, args.box_id)

        context['boxes_path'] = os.path.join(ebx_path, boxes)
        context['scripts'] = scripts
        context['ports'] = ports
        context['boxes'] = box_collection

        filename = os.path.join(ebx_path, args.box_id + '.dockerfile')
        with open(filename, 'w') as dockerfile:
            _generate_dockerfile(context, dockerfile)

        try:
            environment = os.environ.copy()
            environment['ELASTICBOX_PATH'] = EBX_CONTAINER_PATH

            if unknown_args:
                subprocess.call(
                    'docker build {0} -f {1} {2}'.format(' '.join(unknown_args), filename, ebx_path),
                    env=environment,
                    cwd=ebx_path,
                    shell=True)
            else:
                subprocess.call(
                    'docker build -f {0} {1}'.format(filename, ebx_path),
                    cwd=ebx_path,
                    shell=True,
                    env=environment)
        finally:
            os.remove(filename)


def _get_setup_data(boxes, box_id, scope=None):
    box = boxes.get_box(box_id)

    scripts = []
    ports = set()
    inner_boxes = set([box['name']])

    pre_install_script = os.path.join(box['name'], 'events', 'pre_install')
    if os.path.exists(os.path.join(boxes.get_path(), pre_install_script)):
        scripts.append({"scope": scope, "path": pre_install_script})

    for variable in box['variables']:
        name = variable['name']
        value = variable['value']

        if variable['type'] == 'Box':
            if scope:
                nested_boxes, nested_scripts, nested_ports = _get_setup_data(
                    boxes, value, "{0}.{1}".format(scope, name))
            else:
                nested_boxes, nested_scripts, nested_ports = _get_setup_data(boxes, value, name)

            scripts = scripts + nested_scripts
            ports = ports.union(nested_ports)
            inner_boxes = inner_boxes.union(nested_boxes)
        elif variable['type'] == 'Port':
            ports.add(value)

    install_script = os.path.join(box['name'], 'events', 'install')
    if os.path.exists(os.path.join(boxes.get_path(), install_script)):
        scripts.append({"scope": scope, "path": install_script})

    return inner_boxes, scripts, ports


def _generate_dockerfile(context, dockerfile):
    environment = Environment(
        loader=FileSystemLoader(EBX_AGENT_DIRECTORY),
        trim_blocks=True)

    print >> dockerfile, environment.get_template('Dockerfile.jinja').render(context)
