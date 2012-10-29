{% include "cilantro/_config.js" %}

// Extends the block to include a namespaced path for project-level modules
require['paths'] = {
    'project': '{{ JAVASCRIPT_URL }}'
};
