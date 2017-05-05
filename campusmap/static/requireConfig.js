var require = {
    baseUrl: '/static',
    paths: {
        almond: 'node_modules/almond/almond',
        bootstrap: 'node_modules/bootstrap/dist/js/bootstrap',
        jquery: 'node_modules/jquery/dist/jquery',
        ol: '//cdn.research.pdx.edu/openlayers/4.1.0/ol',
        text: 'node_modules/text/text',
        campusmap: '.'
    },
    shim: {
        bootstrap: {
            deps: ['jquery']
        }
    }
};
