# Name of the dos-ini file containing the harvest config files
HARVESTRC_PATH = '.harvestrc'

# Name of the default template repo
TEMPLATE_REPO = 'harvest-template'

TEMPLATE_REPO_DEFAULT_VERSION = 'HEAD'

TEMPLATE_REPO_URL = 'https://github.com/cbmi/' + TEMPLATE_REPO

# Template URL for generating a patch for the diff range
TEMPLATE_PATCH_URL = TEMPLATE_REPO_URL + '/compare/{0}...{1}.patch'

# Template URL for downloading an archive (zip) of a specific version of the template
TEMPLATE_ARCHIVE_URL = TEMPLATE_REPO_URL + '/archive/{0}.zip'

# Template string for the name of the archive
TEMPLATE_ARCHIVE = TEMPLATE_REPO + '-{0}.zip'
