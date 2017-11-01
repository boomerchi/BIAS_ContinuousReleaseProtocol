#!/bin/bash

set -e

CHANGED_FILES=`git diff --name-only HEAD~1..HEAD`
CODE_UPDATE=False
IJMACRO=".ijm"
MATLAB=".m"
echo $CHANGED_FILES
for CHANGED_FILE in $CHANGED_FILES; do
  if [[ $CHANGED_FILE =~ $IJMACRO ]]; then
    CODE_UPDATE=True
    break
  fi
  if [[ $CHANGED_FILE =~ $MATLAB ]]; then
    CODE_UPDATE=True
    break
  fi
done

if [[ $CODE_UPDATE == False ]]; then
  echo "No code updates, exiting"
  exit 1
else
  echo "Code change detected"
fi