#!/bin/sh

setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
}

commit_website_files() {
  git checkout struct_authorea
  git add . *.tex
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
  git remote add origin-pages https://${GH_TOKEN}@github.com/miura/mod3conversionTest2
.git > /dev/null 2>&1
  git push --quiet --set-upstream origin-pages struct_authorea 
}

setup_git
commit_website_files
upload_files