from __future__ import print_function
import os
import sh
import json
import shutil
import tempfile
from zipfile import ZipFile
from .constants import (TEMPLATE_RELEASES_API_URL, GITHUB_API_BETA_ACCEPT,
        TEMPLATE_ARCHIVE_NAME, TEMPLATE_ARCHIVE_URL)

# In process cache to prevent redundant web requests
_versions_cache = None
_template_cache = {}

def find_replace(directory, reps):
    "Recursively replace file contents and/or rename directories."
    renamings = []

    # Walk directory and replace all occurrences
    for root, dirs, files in os.walk(os.path.abspath(directory)):
        for pre, post in reps:
            if pre in dirs:
                renamings.append((root, pre, post))
        for fname in files:
            fpath = os.path.join(root, fname)
            with open(fpath) as f:
                s = f.read()
            for pre, post in reps:
                s = s.replace(pre, post)
            with open(fpath, 'w') as f:
                f.write(s)

    # Rename the more nested directories first
    renamings.reverse()

    # Rename directories
    for root, pre, post in renamings:
        pre = os.path.join(root, pre)
        post = os.path.join(root, post)
        os.rename(pre, post)

def zip_files(name, path):
    "Zip all files under `path` into `archive`."
    zf = ZipFile(name, 'w')
    for root, dirs, files in os.walk(path):
        for f in files:
            zf.write(os.path.join(root, f))
    zf.close()

def cmp_semver(x, y):
    "Compare function for semantic version strings."
    return cmp([int(t) for t in x.split('.')], [int(t) for t in y.split('.')])

def fetch_template_versions():
    "Fetches and sorts the release versions for the Harvest template."
    global _versions_cache

    if _versions_cache is None:
        cmd = sh.curl(TEMPLATE_RELEASES_API_URL,
                H='Accept: {0}'.format(GITHUB_API_BETA_ACCEPT))
        versions = json.loads(cmd.stdout)
        _versions_cache = tuple(sorted([v['tag_name'] for v in versions],
                cmp=cmp_semver, reverse=True))
    return _versions_cache

def fetch_template_archive(version):
    global _template_cache

    if version in _template_cache:
        # Ensure it still exists since this is using temporary filesystem cache
        if os.path.exists(_template_cache[version][0]):
            return _template_cache[version]

    fh, tmp_file = tempfile.mkstemp(suffix='.zip')
    # Close the file handler since it is not being used
    os.close(fh)

    # Fetch template archive and write to temp directory
    sh.wget(TEMPLATE_ARCHIVE_URL.format(version), output_document=tmp_file)

    # Cache the location
    _template_cache[version] = tmp_file

    return _template_cache[version]

def extract_template_archive(archive_path, path):
    # Extract contents into temporary directory
    archive = ZipFile(archive_path)
    tmpdir = tempfile.mkdtemp()
    archive.extractall(tmpdir)

    # Get directory name in zip file since it's variable based on the
    # release version.
    template_dir = ZipFile(archive_path).namelist()[0].rstrip('/')

    # Rename/move nested template directory to path
    os.rename(os.path.join(tmpdir, template_dir), path)

    # Clean up temp directory
    shutil.rmtree(tmpdir)
