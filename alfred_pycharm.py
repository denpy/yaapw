#!/usr/bin/env python
#
# https://github.com/denpy/yaapw
#
"""
Script that filters project names from Pycharm menu items and prints them according to Alfred "Script Filter input"
format (more info https://www.alfredapp.com/help/workflows/inputs/script-filter/), so Alfred will be able to present
them in its UI
"""
import argparse
import json
import os
import re
from typing import Any, Dict, List, Union

THIS_SCRIPT_VERSION = (2020, 10)
THIS_SCRIPT_VERSION_STR = '.'.join([str(d) for d in THIS_SCRIPT_VERSION])

SKIP_PROJECTS = os.getenv('SKIP_PROJECTS')
MENU_ITEMS_DELIMITER = os.getenv('IFS')


def make_menu_items(messages):
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
            # the message case insensitively and by partial worlds too.
            # For example when you type "production" Alfred will find "Music Production" as well
            match=' '.join(re.split(r'[\W\-_,]+', os.path.basename(msg))).lower())

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


def filter_proj_names(items: str, items_2_skip: List[str]) -> List[str]:
    """
    Filter project names from Pycharm menu items
    :param items: Pycharm menu items
    :param items_2_skip: Menu items to filter out
    :return: project names
    """
    proj_names = []
    items = items.strip('\n').split(MENU_ITEMS_DELIMITER)
    for menu_item in items:
        menu_item = menu_item.strip()

        # In order to get currently opened projects we need to traverse Pycharm "Window" menu, project names appear
        # after "Previous Project Window" option, so once we see it we discard all previous items since they are not
        # project names
        if menu_item == 'Previous Project Window':
            proj_names.clear()
            continue

        if menu_item in items_2_skip:
            continue
        proj_names.append(menu_item)

    return proj_names


# noinspection PyShadowingNames
def main(args):
    window_menu_items = args.opened_proj  # Items from "Window" menu
    open_recent_menu_items = args.recent_proj  # Items from "File->Open recent" menu
    if window_menu_items is not None:
        opened_proj_names = filter_proj_names(window_menu_items, ['missing value'])
        print_msg(opened_proj_names)
    elif open_recent_menu_items is not None:
        recent_proj = filter_proj_names(open_recent_menu_items, ['missing value', 'Manage Projects...'])
        print_msg(recent_proj)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This script allows to open recent on currently open Pycharm project',  add_help=True)
    parser.add_argument(
        '--version', '-v', '-V', action='version', help='This script version', version=THIS_SCRIPT_VERSION_STR)

    # Create a group of mutually exclusive args (at least one is required)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--opened-proj', '-o', help='List currently opened projects')
    group.add_argument('--recent-proj', '-r', help='List recent projects')

    args = parser.parse_args()
    main(args)
