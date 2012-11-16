from __future__ import print_function
import re
import os
import sys
import harvest
from fabric.api import local, hide
from fabric.colors import red, green
from harvest.decorators import cli, virtualenv
from harvest.utils import create_virtualenv, managepy_chmod

__doc__ = """\
Creates and sets up a new Harvest project.
"""

HARVEST_TEMPLATE_PATH = os.path.join(os.path.abspath(os.path.dirname(harvest.__file__)), 'template')
STARTPROJECT_ARGS = '--template {0} -e py,ini,gitignore,in,conf,md,sample ' \
    '-n Makefile'.format(HARVEST_TEMPLATE_PATH)


def valid_name(name):
    if re.match(r'^[a-z_]\w*$', name, re.I) is not None:
        return True
    return False


@cli(description=__doc__)
def parser(options):
    project_name = options.project_name
    create_env = options.create_env
    allow_input = options.allow_input
    verbose = options.verbose

    if not valid_name(project_name):
        print(red("Error: The project name '{0}' must be a valid Python "
            "identifier.".format(project_name)))
        sys.exit()

    # Ensure the name does not conflict with an existing Python module
    try:
        __import__(project_name)
        print(red("Error: The project name '{0}' conflicts with an existing "
            "Python module. Please choose another name.".format(project_name)))
        sys.exit()
    except ImportError:
        pass

    hidden_output = []

    if verbose < 1:
        hidden_output.append('stdout')
    if verbose < 2:
        hidden_output.append('running')

    print(green("Setting up project '{0}'...".format(project_name)))

    env_path = '.'
    full_env_path = None

    # Check for virtualenv
    if create_env:
        env_path = '{0}-env'.format(project_name)
        full_env_path = os.path.abspath(env_path)

    @virtualenv(full_env_path)
    def install_django():
        print(green('- Installing Django'))
        local('pip install "django>=1.4,<1.5"')

    @virtualenv(full_env_path)
    def create_project(project_name):
        print(green("- Creating new Harvest project '{0}'".format(project_name)))
        local('django-admin.py startproject {0} {1}'.format(STARTPROJECT_ARGS, project_name))

    @virtualenv(full_env_path)
    def install_deps():
        print(green('- Downloading and installing dependencies'))
        local('pip install -r requirements.txt')

    @virtualenv(full_env_path)
    def collect_static():
        print(green('- Collecting static files'))
        local('make collect')

    @virtualenv(full_env_path)
    def syncdb(allow_input):
        print(green('- Setting up a SQLite database'))
        cmd = './bin/manage.py syncdb --migrate'
        if not allow_input:
            cmd += ' --noinput'
        local(cmd)

    with hide(*hidden_output):
        if create_env:
            create_virtualenv(env_path)

        install_django()

        create_project(project_name)

        # Change into project directory for next set of commands..
        os.chdir(project_name)

        # Ensure manage.py is executable..
        managepy_chmod()

    with hide('running'):
        install_deps()

    with hide(*hidden_output):
        collect_static()

    hidden_output = ['running']
    if not allow_input:
        hidden_output.append('stdout')

    # Refrain from blocking stdout due to the prompts..
    with hide(*hidden_output):
        syncdb(allow_input)

    print(green('\nComplete! Copy and paste the following in your shell:\n'))

    if create_env:
        print(green('cd {0}/{1}\nsource ../bin/activate'.format(env_path, project_name)))
    else:
        print(green('cd {0}'.format(project_name)))

    print(green('./bin/manage.py runserver'))
    print(green('\nOpen up a web browser and go to: http://localhost:8000\n'))


parser.add_argument('project_name', help='Name of the Harvest project. This '
    'must be a valid Python identifier.')
parser.add_argument('-v', '--verbose', action='count',
    help='Print stdout output during installation process.')
parser.add_argument('--no-env', action='store_false', dest='create_env',
    help='Prevents creating a virtualenv and sets up the project in the '
        'current directory.')
parser.add_argument('--no-input', action='store_false', dest='allow_input',
    help='Prevents interactive prompts during setup.')
