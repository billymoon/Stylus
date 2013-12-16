module.exports = function(grunt){
    
    // This will go through package.json and load grunt task
    require("matchdep").filterDev("grunt-*").forEach(grunt.loadNpmTasks);
    
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        convert: {
            yaml2plist: {
                src: ['Stylus.language.yml'],
                dest: 'Stylus.plist'
            }
        },

        rename: {
            move: {
                src: 'Stylus.plist',
                dest: 'Stylus.tmLanguage'
            }
        },
        
        watch: {
            html: {
                files: ['Stylus.language.yml'],
                tasks: ['default']
            }
        }
    });
    grunt.registerTask('default', ['convert', 'rename']);

};
