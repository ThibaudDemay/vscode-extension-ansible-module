#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: vscode_ext
short_description: Manage Visual Studio Code Extension 
description:
  - Add or remove extensions within a Visual Studio Code
version_added: "1.0.0"
options:
  username:
    required: true
    description:
      - Username of users used to install. 
      - To operate on several users this can accept a comma separated list of usernames or a list of usernames.
    aliases: ['users', 'user', 'usernames']
  extension:
    required: true
    description:
      - Extension of Visual Studio Code you want to install.
      - To operate on several extensions this can accept a comma separated list of extensions or a list of extensions.
    aliases: ['exts', 'ext', 'extensions']
  state:
    required: false
    choices: ['present', 'absent']
    default: present
    description:
      - present handles checking existence or getting if definition extension provided,
        absent handles deleting extension.

requirements:
  - code

author:
  - Thibaud Demay (@ThibaudDemay)
"""

from ansible.module_utils.basic import AnsibleModule

def run_module():
    module = AnsibleModule(argument_spec={})
	  response = {"changed": False, "message": "goodbye"}
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
