module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({

    pkg: grunt.file.readJSON('package.json'),

    source_dir: 'src',
    vendor_dir: 'bower_components',
    release_dir: 'app',

    source_files: {
      js: ['**/*.js'],
      css: ['**/*.css'],
      html: ['**/*.html'],
    },
    vendor_files: {
      js: [
        'select2/select2.js',
        'jQuery/jquery.js',
        'angular/angular.js',
        'angular-ui-select2/src/select2.js',
        'angular-resource/angular-resource.js',
        'angular-route/angular-route.js',
        'tipsy/src/javascripts/jquery.tipsy.js',
      ],
      css: [
        'select2/select2.css',
        'tipsy/src/stylesheets/tipsy.css',
      ],
      img: [
        'select2/select2.png',
        'select2/select2-spinner.gif',
        'tipsy/src/images/tipsy.gif',
      ],
    },

    jshint: {
      files: [
        'Gruntfile.js',
        '<%= source_dir %>/<%= source_files.js %>'
      ],
    },

    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      },
      files: {
        expand: true,
        cwd: '<%= source_dir %>/',
        src: '<%= source_files.js %>',
        dest: '<%= release_dir %>/',
        ext: '.min.js',
      },
    },
    copy: {
      app_scripts: {
        files: [
          {
            expand: true,
            cwd: '<%= source_dir %>/',
            src: ['<%= source_files.js %>'],
            dest: '<%= release_dir %>/',
          },
        ],
      },
      app_styles: {
        files: [
          {
            expand: true,
            cwd: '<%= source_dir %>/',
            src: ['<%= source_files.css %>'],
            dest: '<%= release_dir %>/',
          },
        ],
      },
      app_templates: {
        files: [
          {
            expand: true,
            cwd: '<%= source_dir %>/',
            src: ['<%= source_files.html %>'],
            dest: '<%= release_dir %>/',
          },
        ],
      },
      vendor_assets: {
        files: [
          {
            expand: true,
            cwd: 'bower_components/',
            src: [
              '<%= vendor_files.js %>',
              '<%= vendor_files.css %>',
              '<%= vendor_files.img %>',
            ],
            dest: '<%= release_dir %>/vendor/',
          },
        ],
      },
    },

    clean: {
      app_scripts: ['<%= release_dir %>/js'],
      app_styles: ['<%= release_dir %>/styles'],
      app_templates: ['<%= release_dir %>/partials'],
      vendor_assets: ['<%= release_dir %>/vendor'],
    },

    watch: {
      app_scripts: {
        files: ['<%= source_dir %>/<%= source_files.js %>'],
        tasks: ['jshint', 'clean:app_scripts', 'copy:app_scripts'],
      },
      app_styles: {
        files: ['<%= source_dir %>/<%= source_files.css %>'],
        tasks: ['clean:app_styles', 'copy:app_styles'],
      },
      app_templates: {
        files: ['<%= source_dir %>/<%= source_files.html %>'],
        tasks: ['clean:app_templates', 'copy:app_templates'],
      },
      vendor_assets: {
        files: ['<%= vendor_dir %>/<%= vendor_files.js %>',
                '<%= vendor_dir %>/<%= vendor_files.css %>',
                '<%= vendor_dir %>/<%= vendor_files.img %>'],
        tasks: ['copy:vendor_assets'],
      },
    },
  });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-copy');

  // Default task(s).
  grunt.registerTask('default', ['jshint', 'clean', 'copy', 'uglify']);

};