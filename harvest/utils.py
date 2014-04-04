import os
import sys
import stat
from fabric.api import local
from fabric.colors import red, green


def create_virtualenv(env_path, venv_wrap=False, project_name=None):
    if os.path.exists(env_path):
        print(red("Error: Cannot create environment '{0}'. A " \
            "directory with the same already exists.".format(env_path)))
        sys.exit()
    print(green("- Setting up a virtual environment '{0}'".format(env_path)))
    if venv_wrap:
        try:
            venv_home = os.environ['WORKON_HOME']
        except:
            print(red("It doesn't appear that you have virtualenvwrapper installed correctly"))
            sys.exit(1)
        env_path = os.path.join(venv_home, project_name)
        local('virtualenv {0}'.format(env_path), shell='/bin/bash')
    else:
        local('virtualenv {0}'.format(env_path), shell='/bin/bash')
        os.chdir(env_path)


def managepy_chmod():
    mode = stat.S_IMODE(os.stat('bin/manage.py').st_mode)
    executable = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    os.chmod('bin/manage.py', mode | executable)
