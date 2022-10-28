#!/usr/bin/env bash

# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

# set interactive mode to enable defining a gsed alias
shopt -s expand_aliases

# we use sed to make in-file text replacements, but sed works differently depending on the version
if ! sed -i '1s/^/test/' $(mktemp) 2> /dev/null; then
    # macOS (BSD) version of sed
    alias gsed="sed -i ''" 
else
    # POSIX compliant version of sed 
    alias gsed="sed -i"
fi

export gsed

hash_comment () {
  if ! grep -q "SPDX-License-Identifier" "$1"
  then
    echo "$1"
    gsed '1i\
    # Copyright 2021 The MLX Contributors\
    #\
    # SPDX-License-Identifier: Apache-2.0\
    ' "$1"
  fi
}

slash_comment () {
  if ! grep -q "SPDX-License-Identifier" "$1"
  then
    echo "$1"
    gsed '1i\
    // Copyright 2021 The MLX Contributors\
    //\
    // SPDX-License-Identifier: Apache-2.0\
    ' "$1"
  fi
}

css_comment () {
  if ! grep -q "SPDX-License-Identifier" "$1"
  then
    echo "$1"
    gsed '1i\
    /*\
    * Copyright 2021 The MLX Contributors\
    *\
    * SPDX-License-Identifier: Apache-2.0\
    */\
    ' "$1"
  fi
}

html_comment () {
  if ! grep -q "SPDX-License-Identifier" "$1"
  then
    echo "$1"
    gsed '1i\
    <!--\
    Copyright 2021 The MLX Contributors\
    \
    SPDX-License-Identifier: Apache-2.0\
    -->\
    ' "$1"
  fi
}

export -f hash_comment slash_comment css_comment html_comment

echo "Adding missing license headers"

# Python, YAML, Bash
find . -type f -not -path '*/temp/*' -a -not -path '*/\.*' -a \( -name '*.py' -o -name '*.yaml' -o -name '*.yml' -o -name '*.sh' \) -exec bash -c 'hash_comment "$0"' {} \;

# Javascript
find . -type f -not -path '*/node_modules/*' -a -not -path '*/temp/*' -a -not -path '*/\.*' -a -not -path '*.bundle.js' -a \( -name '*.js' -o -name '*.ts' \) -exec bash -c 'slash_comment "$0"' {} \;

# CSS
find . -type f -not -path '*/temp/*' -a -not -path '*/\.*' -a \( -name '*.css' -o -name '*.tsx' \) -exec bash -c 'css_comment "$0"' {} \;

# HTML
find . -type f -not -path '*/temp/*' -a -not -path '*/\.*' -a -name '*.html' -exec bash -c 'html_comment "$0"' {} \;
