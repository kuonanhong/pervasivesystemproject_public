/*jslint node: true, nomen: true */
"use strict";

var gulp = require('gulp'),
    path = require('path'),
    rimraf = require('gulp-rimraf'),
    rename = require('gulp-rename'),
    minifyCss = require('gulp-cssnano'),
    sourcemaps = require('gulp-sourcemaps'),
    browserify = require('browserify'),
    source = require('vinyl-source-stream'),
    buffer = require('vinyl-buffer'),
    minifyjs = require('gulp-uglify'),
    extractor = require('gulp-extract-sourcemap'),
    merge = require('merge-stream');

gulp.task('clean', function () {
    return gulp.src('./public/*', {read: false, dot: true}).pipe(rimraf({ force: true }));
});

gulp.task('html', function () {
    return gulp.src('./client/index.html')
        .pipe(gulp.dest('./public'));
});

gulp.task('css2', function () {
    return gulp.src('./client/style/style.css')
        .pipe(gulp.dest('./public/css'));
});


gulp.task('images', function () {
    return gulp.src('./client/images/**')
        .pipe(gulp.dest('./public/images'));
});


gulp.task('css', function () {
    return merge(
        gulp.src(['./node_modules/jquery/dist/jquery.js',
                './node_modules/bootstrap/dist/js/bootstrap.js',
                './node_modules/knockout/build/output/knockout-latest.js',
                './node_modules/ko-component-router/dist/ko-component-router.js'])
                .pipe(sourcemaps.init())
                .pipe(minifyjs())
                .pipe(rename({suffix: '.min'}))
                .pipe(sourcemaps.write('./'))
                .pipe(gulp.dest('./public/vendor')),
        gulp.src('./node_modules/bootstrap/dist/css/bootstrap.css')
                .pipe(sourcemaps.init())
                .pipe(minifyCss({compatibility: 'ie8'}))
                .pipe(rename({suffix: '.min'}))
                .pipe(sourcemaps.write('./'))
                .pipe(gulp.dest('./public/css')),
        gulp.src('./node_modules/bootstrap/dist/fonts/**').pipe(gulp.dest('./public/fonts'))
    );
});

gulp.task('js', function () {
    return browserify({
        entries: './client/js/index.js',
        debug: true,
    })
        .transform('exposify', {
            expose: {
                'jquery': '$',
                'knockout': 'ko'
            }
        })
        .transform('stringify', {
            extensions: ['.html'],
            minify: false,
            minifyOptions: {
                removeComments: false
            }
        })
        .bundle()
        .pipe(source('index.js'))
        .pipe(buffer())
        .pipe(extractor({
            basedir: path.join(__dirname, './client/js/'),
            fakeFix: true
        }))
        .pipe(gulp.dest('./public/js'));
});

gulp.task('build', ['html', 'js', 'css', 'css2', "images"]);

gulp.task('default', ['clean'], function () {
    return gulp.start('build');
});
