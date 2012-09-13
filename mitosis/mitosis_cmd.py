#!/usr/bin/env python

import argparse
import os
import sys

from mitosis.connect import daughter, mother
from mitosis.settings import VERSION


command_list = {
    'mother': mother,
    'daughter': daughter
}


def print_commands():
    print "The mitosis commands are:"
    commands = command_list.keys()
    for command in commands:
        print "\t{}".format(command)


def valid_command(command_name):
    """Checks that the given command name exists"""
    try:
        return command_list[command_name]
    except KeyError:
        msg = '<{}> is an invalid command'.format(command_name)
        raise argparse.ArgumentTypeError(msg)


if __name__ == '__main__':
    """ For more information write:
            python mitosis.py -h
    """
    parser = argparse.ArgumentParser(description='Creates a mitosis instance')
    parser.add_argument('command', type=valid_command, nargs='?',
                        help='The mitosis command')
    parser.add_argument('-l', '--list', action='store_true',
                        help='Prints all the mitosis commands')
    parser.add_argument('--version', action='store_true',
                        help='Prints the mitosis current version ')

    try:
        arg_dict = vars(parser.parse_args())
    except argparse.ArgumentError as e:
        print e
        sys.exit()

    if arg_dict['version']:
        print "mitosis version {}".format(VERSION)
        sys.exit()
    elif arg_dict['list']:
        print_commands()
        sys.exit()
    if arg_dict['command'] is not None:
        arg_dict['command'].run()
    else:
        print "argument command: <> is an invalid command"
