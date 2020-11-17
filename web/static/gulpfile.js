'use strict';
 
var gulp = require('gulp');
var sass = require('gulp-sass');
var browserSync = require('browser-sync').create();
var autoprefixer = require('gulp-autoprefixer');
 
sass.compiler = require('node-sass');
 
//sass task
gulp.task('sass', function () {
  return gulp.src('./sass/main.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest('./css'))
    .pipe(browserSync.stream());
});
 
//browser sync
gulp.task('browser-sync', function() {
    browserSync.init({
        server: {
            baseDir: "./"
        }
    });

    gulp.watch('./sass/**/*.scss', gulp.series('sass'));
    gulp.watch("./*.html").on('change', browserSync.reload);
});

//browser prefixing
gulp.task('prefix', function () {
  return gulp.src('./css/main.css')
    .pipe(autoprefixer({
        browsers: 'last 2 version',
    }))
    .pipe(gulp.dest('./css'))
});

//production task
gulp.task('production', gulp.series('sass', 'prefix'))