#!/bin/bash
#
# Copyright 2021 IBM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script checks whether any of the files related to the backend docker
# build (files listed in files_to_check) have been modified from the
# origin/master branch. This is done by running a diff on each file between the
# most recent commit on origin/master and HEAD.
#
# Execute from top-level directory i.e. dashboard/
#
# If no changes were detected, return exit code 0.
# If any changes were detected in any of the files, return exit code
# DIFF_DETECTED_ERR_CODE.
# If runtime error occurs, script should fail and return error code.

set -ev

DIFF_DETECTED_ERR_CODE=${DIFF_DETECTED_ERR_CODE:-169}
DIFF_DIR=${DIFF_DIR:-.}

git_url="git://github.com/machine-learning-exchange/mlx.git"

latest_commit=$(git ls-remote ${git_url} | grep HEAD | cut -f 1)

echo "Latest upstream commit: ${latest_commit}"

files_to_check=(${DIFF_DIR})

for file in ${files_to_check[@]}
do
    # Make sure to fetch git_url to make sure this commit exists
    diff_output=$(git diff ${latest_commit} HEAD -- $file)
    if [[ -n "${diff_output}" ]]
    then
        echo "Diff detected in $file"
        exit $DIFF_DETECTED_ERR_CODE
    fi
done

echo "No diffs detected!"

# Should exit with code 0 anyways, but let's explicitly state it here.
exit 0
