require(['cilantro', 'project/csrf'], function(c) {

    c.router.register([
        {
            id: 'query',
            route: 'query/',
            navigable: true,
            view: new c.ui.QueryWorkflow
        }, {
            id: 'results',
            route: 'results/',
            navigable: true,
            view: new c.ui.ResultsWorkflow
        }
    ]);

    return Backbone.history.start({
        pushState: true,
        root: c.getOption('routes.root')
    });

});
