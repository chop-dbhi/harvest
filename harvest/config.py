import os
import ConfigParser
from .constants import HARVESTRC_PATH

class HarvestConfig(object):
    """Dict-like object for the Harvest project's configuration options.
    This interfaces with a dos-ini file.
    """
    def __init__(self, path=None):
        self.path = path
        self.parser = ConfigParser.ConfigParser()
        self.read()

        self.default_section = 'harvest'

        # Ensure the default section is defined
        if not self.parser.has_section(self.default_section):
            self.parser.add_section(self.default_section)

    @property
    def rcpath(self):
        if self.path:
            return os.path.join(self.path, HARVESTRC_PATH)

    def __getitem__(self, key):
        try:
            return self.parser.get(self.default_section, key)
        except ConfigParser.NoOptionError:
            raise KeyError(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def set(self, key, value):
        self.parser.set(self.default_section, key, value)

    def write(self):
        with open(self.rcpath, 'w') as f:
            self.parser.write(f)

    def exists(self):
        "Returns true if the config exists on the filesystem."
        if self.path:
            return os.path.exists(self.rcpath)
        return False

    def read(self):
        "Re-reads the config file."
        if self.rcpath:
            self.parser.read(self.rcpath)
