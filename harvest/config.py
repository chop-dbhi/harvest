# Name of the dos-ini file containing the harvest config files
HARVESTRC_PATH = '.harvestrc'

DEFAULT_PACKAGE_NAME = 'harvest_project'

GITHUB_API_BETA_ACCEPT = 'application/vnd.github.manifold-preview'

GITHUB_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

# Name of the default template repo
TEMPLATE_REPO = 'harvest-template'

# API URL for all releases for template repo
TEMPLATE_RELEASES_API_URL = 'https://api.github.com/repos/cbmi/' + TEMPLATE_REPO + '/releases'

TEMPLATE_REPO_URL = 'https://github.com/cbmi/' + TEMPLATE_REPO

# Template URL for generating a patch for the diff range
TEMPLATE_PATCH_URL = TEMPLATE_REPO_URL + '/compare/{0}...{1}.patch'

# Template URL for downloading an archive (zip) of a specific version of the template
TEMPLATE_ARCHIVE_URL = TEMPLATE_REPO_URL + '/archive/{0}.zip'

# Template string for the name of the archive
TEMPLATE_ARCHIVE = TEMPLATE_REPO + '-{0}.zip'
