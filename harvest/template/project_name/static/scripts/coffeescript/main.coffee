# The modules defined here are included in Cilantro. All project-level modules
# must be access via the namespaced path '{{ project_name }}/main'. This is to
# ensure modules of the same name do not conflict Cilantro's modules.

define [
    'environ'
    'jquery'
    'underscore'
    'backbone'
], (environ, $, _, Backbone) ->
