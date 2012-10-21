// RequireJS optimization configuration
// Full example: https://github.com/jrburke/r.js/blob/master/build/example.build.js

({
    // Optimize relative to this url (i.e. the current directory)
    baseUrl: '.',
    
    // The source directory of the modules
    appDir: 'src',

    // The target directory of the optimized modules
    dir: 'min',

    optimize: 'uglify',

    optimizeCss: 'none',

    paths: {},

    name: 'main'
})
