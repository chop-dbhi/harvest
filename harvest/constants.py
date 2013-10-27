# Name of the dos-ini file containing the harvest config files
HARVESTRC_PATH = '.harvestrc'

# Signifies the first version upgrades are supported.
UPGRADE_SUPPORTED_VERSION = '2.1.0'

# Default package name in harvest-template repo
DEFAULT_PACKAGE_NAME = 'harvest_project'

GITHUB_API_BETA_ACCEPT = 'application/vnd.github.manifold-preview'

# Name of the default template repo
TEMPLATE_REPO_NAME = 'harvest-template'

# API URL for all releases for template repo
TEMPLATE_RELEASES_API_URL = 'https://api.github.com/repos/cbmi/' + TEMPLATE_REPO_NAME + '/releases'

# URL of the template repo
TEMPLATE_REPO_URL = 'https://github.com/cbmi/' + TEMPLATE_REPO_NAME

# Template URL for generating a patch for the diff range
TEMPLATE_PATCH_URL = TEMPLATE_REPO_URL + '/compare/{0}...{1}.patch'

# Template URL for downloading an archive (zip) of a specific version of the template
TEMPLATE_ARCHIVE_URL = TEMPLATE_REPO_URL + '/archive/{0}.zip'

# Template string for the name of the archive
TEMPLATE_ARCHIVE_NAME = TEMPLATE_REPO_NAME + '-{0}.zip'
