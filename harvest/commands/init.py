from __future__ import print_function
import re
import os
import sys
import stat
import harvest
from functools import wraps
from fabric.api import prefix, local, hide
from fabric.colors import red, green
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


def create_virtualenv(env_path):
    if os.path.exists(env_path):
        print(red("Error: Cannot create environment '{}'. A " \
            "directory with the same already exists.".format(env_path)))
        sys.exit()
    print(green("Setting up a virtual environment '{}'...".format(env_path)))
    local('virtualenv {}'.format(env_path))
    os.chdir(env_path)


def managepy_chmod():
    mode = stat.S_IMODE(os.stat('bin/manage.py').st_mode)
    executable = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    os.chmod('bin/manage.py', mode | executable)


def virtualenv(path):
    "Wraps a function and prefixes the call with the virtualenv active."
    if path is None:
        activate = None
    else:
        activate = os.path.join(path, 'bin/activate')

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if path is not None:
                with prefix('source {}'.format(activate)):
                    func(*args, **kwargs)
            else:
                func(*args, **kwargs)
        return inner
    return decorator


@cli(description=__doc__)
def parser(options):
    project_name = options.project_name
    create_env = options.create_env
    allow_input = options.allow_input
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
        env_path = '.'
        full_env_path = None

        # Check for virtualenv
        if create_env:
            env_path = '{}-env'.format(project_name)
            full_env_path = os.path.abspath(env_path)
            create_virtualenv(env_path)

        @virtualenv(full_env_path)
        def install_django():
            print(green('Installing Django...'))
            local('pip install "django>=1.4,<1.5"')

        @virtualenv(full_env_path)
        def create_project(project_name):
            print(green("Creating new Harvest project '{}'...".format(project_name)))
            local('django-admin.py startproject {} {}'.format(STARTPROJECT_ARGS, project_name))

        @virtualenv(full_env_path)
        def install_deps():
            print(green('Downloading and installing dependencies...'))
            local('pip install -r requirements.txt')

        @virtualenv(full_env_path)
        def collect_static():
            print(green('Collecting static files...'))
            local('make collect')

        @virtualenv(full_env_path)
        def syncdb(allow_input):
            print(green('Setting up a SQLite database...'))
            cmd = './bin/manage.py syncdb --migrate'
            if not allow_input:
                cmd += ' --noinput'
            local(cmd)

        install_django()

        create_project(project_name)

        # Change into project directory for next set of commands..
        os.chdir(project_name)

        # Ensure manage.py is executable..
        managepy_chmod()

        install_deps()

        collect_static()

    hidden_output = ['running']
    if not allow_input:
        hidden_output.append('stdout')

    # Refrain from blocking stdout due to the prompts..
    with hide(*hidden_output):
        syncdb(allow_input)

    print(green('\nComplete! Copy and paste the following in your shell:\n'))

    if create_env:
        print(green('cd {}/{}\nsource ../bin/activate'.format(env_path, project_name)))
    else:
        print(green('cd {}'.format(project_name)))

    print(green('./bin/manage.py runserver'))
    print(green('\nOpen up a web browser and go to: http://localhost:8000\n'))


parser.add_argument('project_name', help='Name of the Harvest project. This '
    'must be a valid Python identifier.')
parser.add_argument('-v', '--verbose', action='store_true',
    help='Print stdout output during installation process.')
parser.add_argument('--no-env', action='store_false', dest='create_env',
    help='Prevents creating a virtualenv and sets up the project in the '
        'current directory.')
parser.add_argument('--no-input', action='store_false', dest='allow_input',
    help='Prevents interactive prompts during setup.')
