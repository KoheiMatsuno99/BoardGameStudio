"""
ElasticBox Confidential
Copyright (c) 2015 All Right Reserved, ElasticBox Inc.

NOTICE:  All information contained herein is, and remains the property
of ElasticBox. The intellectual and technical concepts contained herein are
proprietary and may be covered by U.S. and Foreign Patents, patents in process,
and are protected by trade secret or copyright law. Dissemination of this
information or reproduction of this material is strictly forbidden unless prior
written permission is obtained from ElasticBox
"""


import keyring

import ebcli


def initialize_parser(subparsers):
    parser = subparsers.add_parser('logout', help='Logout from ElasticBox')
    parser.set_defaults(func=execute_command)


def execute_command(_args, _unknown):
    password = keyring.get_password(
        ebcli.ELASTICBOX_CREDENTIALS_NAME,
        ebcli.ELASTICBOX_CREDENTIALS_ACCOUNT,
    )
    if password is None:
        print "Not logged in to https://cam.ctl.io"
    else:
        chunks = password.split(',')

        keyring.delete_password(
            ebcli.ELASTICBOX_CREDENTIALS_NAME,
            ebcli.ELASTICBOX_CREDENTIALS_ACCOUNT,
        )
        print "Remove login credentials for {0}".format(chunks[1])
