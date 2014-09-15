import os
import shutil
import subprocess
import unittest

HARVEST_BIN = os.path.join(os.path.dirname(__file__), 'bin/harvest')
TEST_PROJECT = 'project'
TEST_PROJECT_ENV = 'project-env'

class FullTestCase(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TEST_PROJECT):
            shutil.rmtree(TEST_PROJECT)
        if os.path.exists(TEST_PROJECT_ENV):
            shutil.rmtree(TEST_PROJECT_ENV)
        if os.path.exists('openmrs-env'):
            shutil.rmtree('openmrs-env')

    tearDown = setUp

    def test_init(self):
        self.assertEqual(subprocess.call([
            'python',
            HARVEST_BIN,
            'init',
            '--no-input',
            TEST_PROJECT,
        ]), 0)
        self.assertTrue(os.path.exists(TEST_PROJECT_ENV))

    def test_init_demo(self):
        self.assertEqual(subprocess.call([
            'python',
            HARVEST_BIN,
            'init-demo',
            'openmrs',
        ]), 0)
        self.assertTrue(os.path.exists('openmrs-env'))

if __name__ == '__main__':
    unittest.main()
