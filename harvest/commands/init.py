from __future__ import print_function
import re
import os
import sys
import stat
import harvest
from fabric.api import prefix
from fabric.operations import local
from fabric.colors import red, green
from fabric.context_managers import hide, lcd
from harvest.decorators import cli

__doc__ = """\
Creates and sets up a new Harvest project.
"""

HARVEST_TEMPLATE_PATH = os.path.join(os.path.abspath(os.path.dirname(harvest.__file__)), 'template')
STARTPROJECT_ARGS = '--template {} -e py,ini,gitignore,in,conf,md,sample ' \
    '-n Makefile'.format(HARVEST_TEMPLATE_PATH)


def valid_name(name):
    if re.match(r'^[a-z_]\w*$', name, re.I) is not None:
        return True
    return False


@cli(description=__doc__)
def parser(options):
    project_name = options.project_name
    create_env = options.create_env
    verbose = options.verbose

    if not valid_name(project_name):
        print(red("Error: The project name '{}' must be a valid Python "
            "identifier.".format(project_name)))
        sys.exit()

    # Ensure the name does not conflict with an existing Python module
    try:
        __import__(project_name)
        print(red("Error: The project name '{}' conflicts with an existing "
            "Python module. Please choose another name.".format(project_name)))
        sys.exit()
    except ImportError:
        pass

    hidden_output = ['running']
    if not verbose:
        hidden_output.append('stdout')

    with hide(*hidden_output):
        # Check for virtualenv
        if create_env:
            env_path = '{}-env'.format(project_name)
            if os.path.exists(env_path):
                print(red("Error: Cannot create environment '{}'. A " \
                    "directory with the same already exists.".format(env_path)))
                sys.exit()
            print(green("Setting up a virtual environment '{}'...".format(env_path)))
            local('virtualenv {}'.format(env_path))
        else:
            env_path = '.'

        with lcd(env_path):
            with prefix('source bin/activate'):
                print(green('Installing Django...'))
                local('pip install "django>=1.4,<1.5"')

                print(green("Creating new Harvest project '{}'...".format(project_name)))
                local('django-admin.py startproject {} {}'.format(STARTPROJECT_ARGS, project_name))
                # Ensure manage.py is executable..
                mode = stat.S_IMODE(os.stat('bin/manage.py').st_mode)
                executable = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
                os.chmod('bin/manage.py', mode | executable)

        with lcd(os.path.join(env_path, project_name)):
            with prefix('source ../bin/activate'):
                print(green('Downloading and installing dependencies...'))
                local('pip install -r requirements.txt')

                print(green('Collecting static files...'))
                local('make collect')

    print(green('Setting up a SQLite database...'))
    with hide('running'):
        with lcd(os.path.join(env_path, project_name)):
            with prefix('source ../bin/activate'):
                local('./bin/manage.py syncdb --migrate')
    print(green('''
Complete! Copy and paste the following in your shell:

cd {}/{}
source ../bin/activate
./bin/manage.py runserver

Then open up a web browser and go to: http://localhost:8000
'''.format(env_path, project_name)))


parser.add_argument('project_name', help='Name of the Harvest project. This '
    'must be a valid Python identifier.')
parser.add_argument('--no-env', action='store_false', dest='create_env',
    default=True, help='Prevents creating a virtualenv and sets up the ' \
    'project in the current directory.')
parser.add_argument('--verbose', action='store_true',
    help='Print stdout output during installation process.')
