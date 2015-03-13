require.config({
    baseUrl: '/static/js',
    paths: {
        bootstrap: '/static/vendor/bootstrap/dist/js/bootstrap.min',
        jquery: '/static/vendor/jquery/dist/jquery.min',
        ol: '/static/vendor/openlayers/build/ol'
    },
    shim: {
        bootstrap: {
            deps: ['jquery']
        }
    }
});

require([
    'map/app'
]);
