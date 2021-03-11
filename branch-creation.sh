#!/bin/bash

source ./.github/CHIPS-config.sh

git branch -a
if [[ `git branch -a 2>&1` = *develop-starter-code* ]]; then
    echo "no need to create a new branch"
else
    echo "need to create new branch"
    git branch develop-starter-code
fi

git checkout develop-starter-code

python3 ./.github/workflows/evaluate-hierarchy.py ./build-starter-code.json

#https://unix.stackexchange.com/questions/422392/delete-all-folders-inside-a-folder-except-one-with-specific-name
echo "LS BEFORE REMOVING"
ls -A

echo "what is inside final_folder"
ls ${final_folder}

echo "what is inside ."

ls .

# find ./ -mindepth 1 ! -regex '^./myfolder/test2\(/.*\)?' -delete
echo "LS AFTER REMOVING"
ls -A

git add -A

git -c user.name="GitHub Actions" -c user.email="actions@github.com" commit -m "${commit_message}" --author="$CURRENT_USER <$CURRENT_USER@users.noreply.github.com>"

git remote add not-ci ${not_ci_repo_ssh}

git fetch --unshallow not-ci

if [[ `git branch -r 2>&1` = *not-ci/develop-starter-code* ]]; then
    echo "pull develop-starter-code"
    PUSH_OPT=""
else
    echo "no need to pull develop-starter-code"
    PUSH_OPT="-u"
fi

git push -f ${PUSH_OPT} not-ci develop-starter-code
