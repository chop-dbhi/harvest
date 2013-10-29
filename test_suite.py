import os
import shutil
import unittest
from zipfile import ZipFile
from harvest.bundle import HarvestBundle
from harvest import utils


class BaseTestCase(unittest.TestCase):
    archive_name = 'test.zip'
    local_dir = 'test-src'

    def setUp(self):
        if os.path.exists(self.archive_name):
            os.remove(self.archive_name)
        if os.path.exists(self.local_dir):
            shutil.rmtree(self.local_dir)

    tearDown = setUp


class HarvestUtilsTestCase(BaseTestCase):
    def test_fetch_template_versions(self):
        versions = utils.fetch_template_versions()
        self.assertTrue('2.1.0' in versions)

    def test_fetch_template_archive(self):
        archive_path = utils.fetch_template_archive('2.1.0')
        self.assertTrue(os.path.exists(archive_path))

    def test_extract_template_archive(self):
        archive_path  = utils.fetch_template_archive('2.1.0')
        utils.extract_template_archive(archive_path, self.local_dir)
        self.assertTrue('requirements.txt' in os.listdir(self.local_dir))


class HarvestBundleTestCase(BaseTestCase):
    def test_new_name(self):
        b = HarvestBundle(name='My New Project!')
        self.assertEqual(b.name, 'My New Project!')
        self.assertEqual(b.package, 'my_new_project')

        # Download template and unzip it into specified path (which is
        # temporary by default)
        b.setup(path=self.local_dir)
        self.assertTrue(b.version is not None)
        self.assertEqual(b.config.get('version'), b.version)
        self.assertTrue(b.package in os.listdir(b.path))

        # Create a zipfile
        b.zip(self.archive_name)
        self.assertTrue(os.path.exists(self.archive_name))

        # Ensure it's populated
        files = ZipFile(self.archive_name).namelist()
        self.assertTrue(len(files))
        self.assertTrue(files[0].startswith(self.local_dir))

    def test_path(self):
        "Create bundle at a specific path."
        b = HarvestBundle(name='My New Project!', path=self.local_dir)
        b.zip(self.archive_name)
        self.assertTrue(os.path.exists(self.archive_name))

    def test_existing(self):
        "Initialize bundle for existing project."
        # Setup new bundle
        b = HarvestBundle(name='My New Project!', path=self.local_dir)
        b.setup()

        # Initialize new bundle for at the same directory
        b2 = HarvestBundle(path=self.local_dir)

        # Ensure the properties are the same
        self.assertEqual(b.path, b2.path)
        self.assertEqual(b.version, b2.version)
        self.assertTrue(b.version is not None)

    def test_upgrade(self):
        "Test bundle upgrade."
        b = HarvestBundle(name='Test Project', path=self.local_dir)
        # One version behind
        b.version = b.available_versions[1]
        # Download and setup
        b.setup()

        # Upgrade to latest
        b.upgrade()
        self.assertEqual(b.version, b.latest_version)
        self.assertEqual(b.config.get('version'), b.version)


if __name__ == '__main__':
    unittest.main()
