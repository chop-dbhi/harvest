from __future__ import print_function
import os
from fabric.operations import local
from harvest.decorators import cli

__doc__ = """\
Updates this Harvest package.
"""


@cli(description=__doc__)
def parser(options):
    bindir = os.path.dirname(local('which harvest', capture=True))
    pip = os.path.join(bindir, 'pip')
    local('{} install -U harvest'.format(pip))
