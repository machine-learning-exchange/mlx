#!/usr/bin/env bash

# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

hash_comment () {
  echo "$1"
  if ! grep -q "SPDX-License-Identifier" "$1"
  then
    sed -i '' '1i\
    # Copyright 2021 The MLX Contributors\
    #\
    # SPDX-License-Identifier: Apache-2.0\
    ' "$1"
  fi
}

slash_comment () {
  echo "$1"
  if ! grep -q "SPDX-License-Identifier" "$1"
  then
    sed -i '' '1i\
    // Copyright 2021 The MLX Contributors\
    //\
    // SPDX-License-Identifier: Apache-2.0\
    ' "$1"
  fi
}

css_comment () {
  echo "$1"
  if ! grep -q "SPDX-License-Identifier" "$1"
  then
    sed -i '' '1i\
    /*\
    * Copyright 2021 The MLX Contributors\
    *\
    * SPDX-License-Identifier: Apache-2.0\
    */\
    ' "$1"
  fi
}

html_comment () {
  echo "$1"
  if ! grep -q "SPDX-License-Identifier" "$1"
  then
    sed -i '' '1i\
    <!--\
     Copyright 2021 The MLX Contributors\
      \
      SPDX-License-Identifier: Apache-2.0\
    -->\
    ' "$1"
  fi
}

export -f hash_comment slash_comment css_comment html_comment

echo "Adding license headers to ..."

# Python, YAML, Bash
echo " - Python, YAML, Shell scripts"
find . -type f -not -path '*/temp/*' -a -not -path '*/\.*' -a \( -name '*.py' -o -name '*.yaml' -o -name '*.yml' -o -name '*.sh' \) -exec bash -c 'hash_comment "$0"' {} \;
find . -type f -not -path '*/temp/*' -a -name '.travis.yml' -exec bash -c 'hash_comment "$0"' {} \;

# Javascript
find . -type f -not -path '*/temp/*' -a -not -path '*/\.*' -a \( -name '*.js' -o -name '*.ts' \) -exec bash -c 'slash_comment "$0"' {} \;

# CSS
find . -type f -not -path '*/temp/*' -a -not -path '*/\.*' -a \( -name '*.css' -o -name '*.tsx' \) -exec bash -c 'css_comment "$0"' {} \;

# HTML
find . -type f -not -path '*/temp/*' -a -not -path '*/\.*' -a -name '*.html' -exec bash -c 'html_comment "$0"' {} \;
