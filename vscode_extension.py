#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Thibaud Demay <demay.thibaud@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: vscode_extension
short_description: Manage Visual Studio Code Extension
description:
  - Add or remove extensions within a Visual Studio Code
version_added: "1.0.0"
options:
  name:
    required: true
    description:
      - Extension of Visual Studio Code you want to install.
      - To operate on several extensions this can accept a comma separated
        list of extensions or a list of extensions.
    type: list
    elements: str
    aliases: ['exts', 'ext', 'extension', 'extensions']
  state:
    required: false
    choices: ['present', 'absent']
    default: present
    type: str
    description:
      - present handles checking existence or getting if definition extension
        provided, absent handles deleting extension.

requirements:
  - code

author:
  - Thibaud Demay (@ThibaudDemay)
"""

EXAMPLES = """
# Add extensions in  Visual Studio Code
- vscode_extension:
  name:
    - ext.test1@version1
    - ext.test2
  state: present

# Remove extensions in Visual Studio Code
- vscode_extension:
  name:
    - ext.test1@version1
    - ext.test2
  state: absent
"""

from ansible.module_utils.basic import AnsibleModule


class VSCodeCLI():

    def __init__(self, module, code_bin):
        self.module = module
        self.bin = code_bin
        self.extensions = []

    def load_extensions(self):
        """
        <visual_studio_code_exec> --list-extensions --show-versions
        """
        exts = []
        cmd = [self.bin, '--list-extensions', '--show-versions']
        rc, out, err = self.module.run_command(cmd)

        if rc == 0:
            for extension in out.split():
                ext = dict()
                ext['raw'] = extension
                ext['name'], ext['version'] = extension.split('@')
                exts.append(ext)

        self.extensions = exts

    def filter_not_install(self, extensions):
        """
        Filter extensions already install to kept only not install extensions
        """
        for c_ext in self.extensions:
            if c_ext['raw'] in extensions:
                extensions.remove(c_ext['raw'])
            elif c_ext['name'] in extensions:
                extensions.remove(c_ext['name'])

        return extensions

    def filter_install(self, extensions):
        """ Filter all extensions install to kept only extensions install """
        c_raw_exts = [c_ext['raw'] for c_ext in self.extensions]
        c_name_exts = [c_ext['name'] for c_ext in self.extensions]

        # make a copy of list before remove items in list
        for ext in extensions[:]:
            if not(ext in c_raw_exts or ext in c_name_exts):
                extensions.remove(ext)

        return extensions

    def install_extension(self, extension):
        """ Install extension in Visual Studio Code
        <visual_studio_code_exec> --install-extension
        """
        cmd = [self.bin, '--force', '--install-extension', extension]
        if self.module.check_mode:
            rc = 0
        else:
            rc, out, err = self.module.run_command(cmd)

        if rc == 0:
            self.load_extensions()
            return rc, ''
        else:
            return rc, out + err

    def uninstall_extension(self, extension):
        """ Uninstall extension in Visual Studio Code
        <visual_studio_code_exec> --uninstall-extension
        """
        cmd = [self.bin, '--force', '--uninstall-extension', extension]
        if self.module.check_mode:
            rc = 0
        else:
            rc, out, err = self.module.run_command(cmd)

        if rc == 0:
            self.load_extensions()
            return rc, ''
        else:
            return rc, out + err


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(
                type='list',
                elements='str',
                aliases=['exts', 'ext', 'extension', 'extensions'],
                required=True
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        ),
        supports_check_mode=True
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    code_bin = module.get_bin_path('code')
    if not code_bin:
        code_bin = module.get_bin_path('code-insiders')

    cli = VSCodeCLI(module, code_bin)

    try:
        wanted_extensions = module.params['name'][:]
        cli.load_extensions()

        if module.params['state'] == 'present':
            extensions_to_install = cli.filter_not_install(wanted_extensions)
            for extension in extensions_to_install:
                rc, msg = cli.install_extension(extension)
                if rc != 0:
                    module.fail_json(msg="Error install Visual Studio Code extension : %s" % msg)
            result['changed'] = len(extensions_to_install) > 0
        elif module.params['state'] == 'absent':
            extensions_to_remove = cli.filter_install(wanted_extensions)
            for extension in extensions_to_remove:
                rc, msg = cli.uninstall_extension(extension)
                if rc != 0:
                    module.fail_json(msg="Error uninstall Visual Studio Code extension : %s" % msg)
            result['changed'] = len(extensions_to_remove) > 0

        module.exit_json(**result)

    except Exception as exc:
        module.fail_json(msg="Exception Unknown : %s" % exc)


if __name__ == '__main__':
    main()
