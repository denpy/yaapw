#!/usr/bin/env python
#
# FOO
#
import argparse
import json
import os
import re
from typing import Any, Dict, List, Union

THIS_SCRIPT_VERSION = (2020, 9)
THIS_SCRIPT_VERSION_STR = '.'.join([str(d) for d in THIS_SCRIPT_VERSION])

SKIP_PROJECTS = os.getenv('SKIP_PROJECTS')
MENU_ITEMS_DELIMITER = os.getenv('IFS')


def make_menu_items(messages):
    # noinspection PyShadowingNames
    def make_menu_item_obj(msg: str) -> Dict[str, Any]:
        """
        Makes a dict with fields that fit Alfred  format
        More about formats:
            https://www.alfredapp.com/help/workflows/inputs/script-filter/json/
        :param msg: a message that will be presented in Alfred
        :return: a dict that contains the messages in a format that Alfred can handle
        """
        # A "template" objects with specific fields for Alfred
        msg_obj = dict(
            title=msg,
            valid=True,
            field_name='title',
            arg=msg,
            autocomplete=msg,
            # Split and lower case the message so when typing in Alfred it will find matching result for any part of
            # the message case insensitively. For example when you type "production" Alfred will find "Music
            # Production" as well
            match=' '.join(re.split(r'\W', msg)).lower())

        return msg_obj.copy()

    # Function entry point
    # Make objects that represent messages of Alfred menu items (dropdown options user see when typing in Alfred)
    return dict(items=[make_menu_item_obj(msg) for msg in messages])


def print_msg(msg_or_msgs: Union[str, list]):
    # noinspection Assert
    assert isinstance(msg_or_msgs, (str, list)), 'Bad parameter type, must be str or list'

    if isinstance(msg_or_msgs, str):
        msg_or_msgs = [msg_or_msgs]
    print(json.dumps(make_menu_items(msg_or_msgs)))


def filter_proj_names(menu_items: str, items_2_skip: List[str]) -> List[str]:
    """
    FOO
    :param menu_items:
    :param items_2_skip:
    :return:
    """
    proj_names = []
    menu_items = menu_items.strip('\n').split(MENU_ITEMS_DELIMITER)
    for menu_item in menu_items:
        menu_item = menu_item.strip()

        # FOO explain this
        if menu_item == 'Previous Project Window':
            proj_names.clear()
            continue

        if menu_item in items_2_skip:
            continue
        proj_names.append(menu_item)

    return proj_names


# noinspection PyShadowingNames
def main(args):
    if args.list_opened is not None:
        opened_proj_names = filter_proj_names(args.list_opened, ['missing value'])
        print_msg(opened_proj_names)
    elif args.list_recent is not None:
        recent_proj = filter_proj_names(args.list_recent, ['missing value', 'Manage Projects...'])
        print_msg(recent_proj)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This script allows to control Endel app playback on macOS',  add_help=True)
    parser.add_argument(
        '--version', '-v', '-V', action='version', help='This script version', version=THIS_SCRIPT_VERSION_STR)

    # Create a group of mutually exclusive args (at least one is required)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list-opened', '-o', help='List currently opened projects')
    group.add_argument('--list-recent', '-r', help='List recent projects')

    args = parser.parse_args()
    main(args)
