from __future__ import print_function
import os
import sys
import json
import urllib2
import datetime
import tempfile
import subprocess
import ConfigParser
from fabric.operations import local
from fabric.context_managers import hide, lcd
from harvest import config
from harvest.decorators import cli

__doc__ = """\
Upgrades an existing Harvest project.
"""

def cmp_semver(x, y):
    return cmp(x.split('.'), y.split('.'))

def fetch_versions():
    versions = json.loads(local('curl -H "Accept: {0}" {1}'.format(
            config.GITHUB_API_BETA_ACCEPT,
            config.TEMPLATE_RELEASES_API_URL), capture=True))
    return sorted([v['tag_name'] for v in versions], cmp=cmp_semver)


@cli(description=__doc__)
def parser(options):
    project_path = options.path
    package_name = options.package_name
    current_version = options.current_version
    upgrade_version = options.upgrade_version
    allow_input = options.allow_input
    verbosity = options.verbosity

    if not os.path.exists(project_path):
        print('Project does not exist at {0}'.format(project_path))
        sys.exit(1)

    # Create config parser for determining the last known state
    cparser = ConfigParser.ConfigParser()
    cparser.read(os.path.join(project_path, config.HARVESTRC_PATH))

    # Harvest related settings
    try:
        harvest_options = dict(cparser.items('harvest'))
    except (ConfigParser.MissingSectionHeaderError, ConfigParser.NoSectionError):
        harvest_options = {}

    # Command-line argument overrides harvestrc
    if not current_version and 'version' in harvest_options:
        current_version = harvest_options['version']
    else:
        print('Harvest project in an unknown state. '
                'Specify --current-version or add a .harvestrc file with '
                'the version specified under the [harvest] section.')
        sys.exit(1)

    if not package_name and 'package' in harvest_options:
        package_name = harvest_options['package']
    else:
        print('Package name required. Specify --package-name or add a '
            '.harvestrc file with `package` specified under the '
            '[harvest] section.')
        sys.exit(1)

    if not upgrade_version:
        versions = fetch_versions()
        upgrade_version = versions[-1]

    patch_url = config.TEMPLATE_PATCH_URL.format(current_version, upgrade_version)

    with tempfile.NamedTemporaryFile() as pfile:
        patch = local('wget -O - {0}'.format(patch_url), capture=True)
        pfile.write(patch.replace(config.DEFAULT_PACKAGE_NAME, package_name))
        pfile.flush()

        # Apply patch, ensure the exit code is clean
        if subprocess.call(['git', 'apply', '--directory', project_path, pfile.name]):
            print('Error applying the patch.')
            sys.exit(1)

    if not cparser.has_section('harvest'):
        cparser.add_section('harvest')
    cparser.set('harvest', 'package', package_name)
    cparser.set('harvest', 'version', upgrade_version)

    with lcd(project_path):
        with open(config.HARVESTRC_PATH, 'w') as rc:
            cparser.write(rc)


parser.add_argument('path', help='Path to the Harvest project to upgrade.')
parser.add_argument('-v', '--verbosity', action='count',
        help='Verbosity of the output.')
parser.add_argument('--package-name', help='The main package name')
parser.add_argument('--current-version', help='The current version of the '
        'Harvest application. Only necessary if no .harvestrc is available.')
parser.add_argument('--upgrade-version', help='The version to upgrade the '
        'Harvest application to. Only necessary if no .harvestrc is available.')
parser.add_argument('--no-input', action='store_false', dest='allow_input',
        help='Prevents interactive prompts during setup.')
