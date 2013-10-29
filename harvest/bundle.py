from __future__ import print_function
import re
import os
import sh
import shutil
import tempfile
from zipfile import ZipFile
from .constants import (TEMPLATE_ARCHIVE_NAME, TEMPLATE_ARCHIVE_URL,
        DEFAULT_PACKAGE_NAME, TEMPLATE_PATCH_URL)
from . import utils
from .contextmanagers import cd
from .config import HarvestConfig

valid_re = re.compile(r'^[a-z_]\w*$', re.I)
prefix_re = re.compile(r'^([^a-z]*)', re.I)
non_anu_re = re.compile(r'([^\w]+)', re.I)


class HarvestBundle(object):
    """A bundle contains all the components for a functioning Harvest
    application. The contents includes:

        * project directory
        * SQLite database for Avocado
        * project-specific settings file

    This does not contain the database itself (unless it is a SQLite uploaded
    database), but contains the connection information in the settings file.

    The bundle can be compressed as a zip-file for distribution.
    """
    def __init__(self, name=None, package=None, version=None, path=None):
        config = HarvestConfig(path)

        # Attempt to get the package from config
        if not package:
            package = config.get('package')

        # Validate the package name if defined, otherwise create one
        if package:
            if not valid_re.match(package):
                raise ValueError('package name is not a valid Python '
                        'identifier: {0}'.format(package))
        elif not name:
            raise ValueError('package name must be supplied')
        else:
            # Replace non-alphanumeric characters with underscore
            package = non_anu_re.sub('_', name).strip('_')

            # Trim invalid prefix
            match = prefix_re.match(package)
            if match:
                prefix = match.groups()[0]
                package = package[len(prefix):]

            # No characters are left!
            if not package:
                raise ValueError('package name could not generated from '
                        'project name')

            package = package.lower()

            # Ensure the name does not conflict with an existing Python module
            # TODO: this could be a tad smarter depending on the path
            try:
                __import__(package)
                raise ValueError('The package name conflicts with an '
                        'existing module.')
            except ImportError:
                pass

        # Attempt to get the version from config, fall back to fetching one
        if not version:
            version = config.get('version')

        self._path = None

        self.name = name
        self.package = package
        self.version = version
        self.config = config
        self.path = path

    def _get_path(self):
        return self._path

    def _set_path(self, path):
        self._path = path
        self.config.path = path

    path = property(_get_path, _set_path)

    @property
    def available_versions(self):
        "Returns a tuple of available versions in descending order."
        return utils.fetch_template_versions()

    @property
    def latest_version(self):
        "Returns the latest release version."
        return self.available_versions[0]

    def is_latest_version(self):
        "Returns true if this project is using the latest release."
        return self.latest_version == self.version

    def setup(self, path=None):
        if self.config.exists():
            return

        version = self.version

        if not version:
            version = self.latest_version

        archive_path = utils.fetch_template_archive(version)

        # Path supplied, otherwise fallback to temp path if none is already set
        if path:
            self.path = path
        elif not self.path:
            self.path = tempfile.mkdtemp()

        utils.extract_template_archive(archive_path, self.path)

        utils.find_replace(self.path, [
            (DEFAULT_PACKAGE_NAME, self.package)
        ])

        self.version = version
        self.config.read()

    def zip(self, filename):
        "Writes the contents of the bundle to a zip file."
        if os.path.exists(filename):
            raise ValueError('{0} already exists'.format(filename))

        # Ensure the bundle is setup
        self.setup()
        filename = os.path.abspath(filename)

        # Temporarily change to source directory while zipping to prevent
        # whole directory tree from being included
        abspath = os.path.abspath(self.path)
        with cd(os.path.dirname(abspath)):
            utils.zip_files(filename, os.path.basename(abspath))

    def upgrade(self, version=None, **options):
        "Upgrades the bundle to the version specified (or the latest)."
        if not self.is_latest_version():
            if not version:
                version = self.latest_version

            # Construct patch URL from current version to the target version
            patch_url = TEMPLATE_PATCH_URL.format(self.version, version)

            # Download and apply patch
            with tempfile.NamedTemporaryFile() as patch:
                output = sh.wget(patch_url, output_document='-').stdout
                # Replace package name with local one
                patch.write(output.replace(DEFAULT_PACKAGE_NAME, self.package))
                # Flush to disk so patch can be applied
                patch.flush()

                try:
                    # Apply patch, ensure the exit code is clean
                    sh.git.apply(patch.name, directory=self.path)
                    self.config.read()
                    self.version = version
                except sh.ErrorReturnCode:
                    print('There was a problem applying the patch.')
                    return

        if options.get('update_deps'):
            self.update_dependencies()

        if options.get('migrate'):
            self.migrate_database()

    def update_dependencies(self):
        "Updates the project's dependencies."
        sh.pip.install(requirement='requirements.txt')

    def migrate_database(self):
        "Performs Harvest-related migrations."
        os.environ['DJANGO_SETTINGS_MODULE'] = '{0}.conf.settings'.format(self.package)
        from django.core import management
        management.call_command('migrate')
