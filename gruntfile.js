module.exports = function(grunt){
        
    // This will go through package.json and load grunt task
    require("matchdep").filterDev("grunt-*").forEach(grunt.loadNpmTasks);
    var stylus = require('stylus'),
        fs = require('fs');

    grunt.registerTask('test', function() {
        var str = fs.readFileSync('./highlight-test.stylus', { encoding: 'utf-8'}),
            done = this.async();
        stylus(str)
            .set('filename', 'test.css')
            .render(function(err, css) {
                if (err) {
                    grunt.log.error(err);
                    done(false);
                } else {
                    done(true);
                }
            });
    });
    
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
            },
            stylus: {
                files: ['highlight-test.stylus'],
                tasks: ['test']
            }
        }
    });
    grunt.registerTask('default', ['convert', 'rename', 'test']);

};
