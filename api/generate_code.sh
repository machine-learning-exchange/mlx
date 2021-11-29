#!/usr/bin/env bash

# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

# define global variables
REPO_URL="https://github.com/machine-learning-exchange/mlx.git"
SCRIPT_DIR="$(cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd)"
PROJECT_DIR="${TRAVIS_BUILD_DIR:-$(cd "${SCRIPT_DIR%/api}"; pwd)}"
TEMP_DIR="${PROJECT_DIR}/temp"
CLONE_DIR="${TEMP_DIR}/mlx_main_latest"
VERSION="main"


#mkdir -p "${CLONE_DIR}"
#git --work-tree="${CLONE_DIR}" checkout HEAD -- api
#cd "${CLONE_DIR}"

clone_repo_to_tempdir() {
  if [ ! -d "${CLONE_DIR}" ]; then
    echo "========================================================================"
    echo "Clone repo into temp dir ..."
    echo "========================================================================"
    git clone "${REPO_URL}" "${CLONE_DIR}" -b "${VERSION}" \
        -c advice.detachedHead=false \
        -c core.sparseCheckout=true \
        --no-checkout \
        --depth=1 \
        --filter=blob:none #-q
    cd "${CLONE_DIR}"
    git config core.sparseCheckout true
    echo "api/*" > .git/info/sparse-checkout
    echo "tools/*" >> .git/info/sparse-checkout
    git checkout main #-- api
    cd - &> /dev/null
  else
    echo "Get latest commit from main ..."
    cd "${CLONE_DIR}"
    git fetch origin # -q
    git -c advice.detachedHead=false checkout "${VERSION}" -f -- api tools #-q
    cd - &> /dev/null
  fi
}

generate_reverse_patch_for_undesired_codegen_results() {
  clone_repo_to_tempdir
  echo "========================================================================"
  echo "Generate reverse-patch for undesired codegen results ..."
  echo "========================================================================"
  cd "${CLONE_DIR}"
  ./api/codegen.sh || exit 1
  ./tools/bash/add_license_headers.sh || exit 1
  #git diff --output="${TEMP_DIR}/undesired_codegen_results_$(date +"%Y-%m-%d").patch"
  git diff -R --output="${TEMP_DIR}/revert_undesired_codegen_results_$(date +"%Y-%m-%d").patch"
  #git checkout .  # undo local changes
  #git clean -fd   # delete untracked files/directories
  cd - &> /dev/null
}

generate_code() {
  echo "========================================================================"
  echo "Generate API code ..."
  echo "========================================================================"
  cd "${PROJECT_DIR}"
  ./api/codegen.sh || exit 1
  ./tools/bash/add_license_headers.sh || exit 1
}

revert_undesired_codegen_results() {
  generate_reverse_patch_for_undesired_codegen_results
  echo "========================================================================"
  echo "Revert undesired codegen results ..."
  echo "========================================================================"
  cd "${PROJECT_DIR}"
  #git apply --whitespace=nowarn --reverse "${TEMP_DIR}/undesired_codegen_results_$(date +"%Y-%m-%d").patch"
  git apply --reject --whitespace=fix "${TEMP_DIR}/revert_undesired_codegen_results_$(date +"%Y-%m-%d").patch"
  echo "========================================================================"
  echo "Files with undesired changes that could not be reverted:"
  echo "========================================================================"
  find .  -name "*.rej" -type f
}

generate_code
revert_undesired_codegen_results

echo "Done"
