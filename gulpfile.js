const gulp = require("gulp");

const css = () => {
  const postCSS = require("gulp-postcss");
  const sass = require("gulp-sass");
  const minify = require("gulp-csso");
  sass.compiler = require("node-sass");
  return gulp
    .src("assets/scss/styles.scss")  //sass파일을 찾는다
    .pipe(sass().on("error", sass.logError))
    .pipe(postCSS([require("tailwindcss"), require("autoprefixer")])) //sass파일을 css로 만든다.
    .pipe(minify()) //간편화
    .pipe(gulp.dest("static/css"));  //css파일에 저장한다. - 이 과정을 npm run css
};

exports.default = css;