#!/usr/bin/env bash

# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

sed_for_linux() {
  sed -i '1i\
  # Copyright 2021 The MLX Contributors\
  #\
  # SPDX-License-Identifier: Apache-2.0\
  ' "$1"
}

sed_for_macos() {
  sed -i '' '1i\
  # Copyright 2021 The MLX Contributors\
  #\
  # SPDX-License-Identifier: Apache-2.0\
  ' "$1"
}

hash_comment () {
  echo "$1"
  if ! grep -q "SPDX-License-Identifier" "$1"
  then
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
      $(sed_for_linux $1)
    elif [[ "$OSTYPE" == "darwin"* ]]; then
      $(sed_for_macos $1)
    else
      echo "FAILED | OS not compatible | Check /hack/add_license_headers.sh "
    fi
  fi
}

slash_comment () {
  echo "$1"
  if ! grep -q "SPDX-License-Identifier" "$1"
  then
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
      $(sed_for_linux $1)
    elif [[ "$OSTYPE" == "darwin"* ]]; then
      $(sed_for_macos $1)
    else
      echo "FAILED | OS not compatible | Check /hack/add_license_headers.sh "
    fi
  fi
}

css_comment () {
  echo "$1"
  if ! grep -q "SPDX-License-Identifier" "$1"
  then
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
      $(sed_for_linux $1)
    elif [[ "$OSTYPE" == "darwin"* ]]; then
      $(sed_for_macos $1)
    else
      echo "FAILED | OS not compatible | Check /hack/add_license_headers.sh "
    fi
  fi
}

html_comment () {
  echo "$1"
  if ! grep -q "SPDX-License-Identifier" "$1"
  then
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
      $(sed_for_linux $1)
    elif [[ "$OSTYPE" == "darwin"* ]]; then
      $(sed_for_macos $1)
    else
      echo "FAILED | OS not compatible | Check /hack/add_license_headers.sh "
    fi
  fi
}

export -f sed_for_linux sed_for_macos hash_comment slash_comment css_comment html_comment

echo "Adding missing license headers"

# Python, YAML, Bash
find . -type f -not -path '*/temp/*' -a -not -path '*/\.*' -a \( -name '*.py' -o -name '*.yaml' -o -name '*.yml' -o -name '*.sh' \) -exec bash -c 'hash_comment "$0"' {} \;

# Javascript
find . -type f -not -path '*/node_modules/*' -a -not -path '*/temp/*' -a -not -path '*/\.*' -a \( -name '*.js' -o -name '*.ts' \) -exec bash -c 'slash_comment "$0"' {} \;

# CSS
find . -type f -not -path '*/temp/*' -a -not -path '*/\.*' -a \( -name '*.css' -o -name '*.tsx' \) -exec bash -c 'css_comment "$0"' {} \;

# HTML
find . -type f -not -path '*/temp/*' -a -not -path '*/\.*' -a -name '*.html' -exec bash -c 'html_comment "$0"' {} \;
