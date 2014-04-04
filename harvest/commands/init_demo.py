from __future__ import print_function
import os
import sys
import urllib2
from zipfile import ZipFile
from fabric.api import local, hide
from fabric.colors import green
from harvest.decorators import cli, virtualenv
from harvest.utils import create_virtualenv, managepy_chmod

__doc__ = """\
Downloads and sets up a Harvest demo locally.
"""


DEMOS = {
    'openmrs': {
        'url': 'https://github.com/cbmi/harvest-openmrs/zipball/demo'
    }
}


def download_demo(demo_name):
    "Downloads and extracts the demo zip file"
    print(green('- Downloading'), end='')
    response = urllib2.urlopen(DEMOS[demo_name]['url'])

    # Extract real name of zipfile
    content_disposition = response.headers.getheader('content-disposition')
    real_name = os.path.splitext(content_disposition.split('; ')[1].split('=')[1])[0]

    fname = '{0}.zip'.format(demo_name)

    # Download zipfile
    with open(fname, 'wb') as tmpfile:
        while True:
            packet = response.read(2 ** 16)
            if not packet:
                print(green('done'))
                break
            tmpfile.write(packet)
            sys.stdout.write(green('.'))
            sys.stdout.flush()
        response.close()

    print(green('- Extracting'))
    # Extract zipfile
    zipfile = ZipFile(fname)
    zipfile.extractall()

    # Clean up and rename to the correct demo name
    os.remove(fname)
    os.rename(real_name, demo_name)


@cli(description=__doc__)
def parser(options):
    demo_name = options.demo_name
    create_env = options.create_env
    verbose = options.verbose
    venv_wrap = options.venv_wrap

    hidden_output = []

    if verbose < 1:
        hidden_output.append('stdout')
    if verbose < 2:
        hidden_output.append('running')

    print(green("Setting up the '{0}' demo...".format(demo_name)))

    env_path = '.'
    full_env_path = None

    # Check for virtualenv
    if create_env:
        if venv_wrap:
            try:
                env_path = os.path.join(os.environ['WORKON_HOME'], demo_name)
            except KeyError:
                print('Virtualenvwrapper WORKON_HOME environment variable not defined')
                raise
        else:
            env_path = '{0}-env'.format(demo_name)

        full_env_path = os.path.abspath(env_path)

    @virtualenv(full_env_path, venv_wrap, demo_name)
    def install_deps():
        print(green('- Downloading and installing dependencies'))
        local('pip install -r requirements.txt', shell='/bin/bash')

    @virtualenv(full_env_path, venv_wrap, demo_name)
    def collect_static():
        print(green('- Collecting static files'))
        local('make collect', shell='/bin/bash')

    with hide(*hidden_output):
        if create_env:
            if venv_wrap:
                create_virtualenv(env_path, venv_wrap=True, demo_name=demo_name)
            else:
                create_virtualenv(env_path)

        # Download the demo
        download_demo(demo_name)

        # Change into project directory for next set of commands..
        os.chdir(demo_name)

        # Ensure manage.py is executable..
        managepy_chmod()

    with hide('running'):
        install_deps()

    with hide(*hidden_output):
        collect_static()

    print(green('\nComplete! Copy and paste the following in your shell:\n'))

    if create_env:
        print(green('cd {0}/{1}\nsource ../bin/activate'.format(env_path, demo_name)))
    else:
        print(green('cd {0}'.format(demo_name)))

    print(green('./bin/manage.py runserver'))
    print(green('\nOpen up a web browser and go to: http://localhost:8000\n'))


parser.add_argument('demo_name', choices=sorted(DEMOS.keys()),
    help='The name of one of the Harvest project demos.')
parser.add_argument('-v', '--verbose', action='count',
    help='Print stdout output during installation process.')
parser.add_argument('--no-env', action='store_false', dest='create_env',
    help='Prevents creating a virtualenv and sets up the project in the '
        'current directory.')
parser.add_argument('-w','--venv-wrap', action='store_true', dest='venv_wrap',
    help='Use target systems instance of virtualenvwrapper to build')
