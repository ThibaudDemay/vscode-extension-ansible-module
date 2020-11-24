# vscode-extension-ansible-module

This Ansible module permit to install or uninstall Visual Studio Code extensions with Ansible.

## Requirements

This module currently working on Ubuntu.
You need to install Visual Studio Code for use this module ([here](https://code.visualstudio.com/docs/setup/linux)).

You can use this module byt placing it in library folder in root of your ansible playbook folder or in roles folder in the role where it is used.

## Install Visual Studio Code extension(s)

```yml
- vscode_extension:
  name:
    - ms-python.python
  state: present
```

## Uninstall Visual Studio Code extension(s)

```yml
- vscode_extension:
  name:
    - ms-python.python
  state: absent
```

## Tips

You can show what extensions was install on your Visual Studio Code with VS Code CLI.

```console
foo@bar:~$ code --list-extensions
ms-python.python
ms-toolsai.jupyter
```