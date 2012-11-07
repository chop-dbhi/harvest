import os
import sys
import stat
from fabric.api import local
from fabric.colors import red, green


def create_virtualenv(env_path):
    if os.path.exists(env_path):
        print(red("Error: Cannot create environment '{0}'. A " \
            "directory with the same already exists.".format(env_path)))
        sys.exit()
    print(green("- Setting up a virtual environment '{0}'".format(env_path)))
    local('virtualenv {0}'.format(env_path))
    os.chdir(env_path)


def managepy_chmod():
    mode = stat.S_IMODE(os.stat('bin/manage.py').st_mode)
    executable = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    os.chmod('bin/manage.py', mode | executable)
