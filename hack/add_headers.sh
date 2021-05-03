# Copyright 2021 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#!/usr/bin/env bash

hash_comment () {
  if ! grep -q "Licensed under the Apache License" $1
  then
    sed -i '' '1i\
    # Copyright 2021 IBM Corporation\
    # \
    # Licensed under the Apache License, Version 2.0 (the "License");\
    # you may not use this file except in compliance with the License.\
    # You may obtain a copy of the License at\
    # \
    #     http://www.apache.org/licenses/LICENSE-2.0\
    # \
    # Unless required by applicable law or agreed to in writing, software\
    # distributed under the License is distributed on an "AS IS" BASIS,\
    # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\
    # See the License for the specific language governing permissions and\
    # limitations under the License.\
    ' $1
  fi
}

slash_comment () {
  if ! grep -q "Licensed under the Apache License" $1
  then
    sed -i '' '1i\
    // Copyright 2021 IBM Corporation\
    // \
    // Licensed under the Apache License, Version 2.0 (the "License");\
    // you may not use this file except in compliance with the License.\
    // You may obtain a copy of the License at\
    // \
    //     http://www.apache.org/licenses/LICENSE-2.0\
    // \
    // Unless required by applicable law or agreed to in writing, software\
    // distributed under the License is distributed on an "AS IS" BASIS,\
    // WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\
    // See the License for the specific language governing permissions and\
    // limitations under the License.\
    ' $1
  fi
}

css_comment () {
  if ! grep -q "Licensed under the Apache License" $1
  then
    sed -i '' '1i\
    /* \
    *  Copyright 2021 IBM Corporation\
    * \
    *  Licensed under the Apache License, Version 2.0 (the "License");\
    *  you may not use this file except in compliance with the License.\
    *  You may obtain a copy of the License at\
    * \
    *      http://www.apache.org/licenses/LICENSE-2.0\
    * \
    *  Unless required by applicable law or agreed to in writing, software\
    *  distributed under the License is distributed on an "AS IS" BASIS,\
    *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\
    *  See the License for the specific language governing permissions and\
    *  limitations under the License.\
    */ \
    ' $1
  fi
}

html_comment () {
  if ! grep -q "Licensed under the Apache License" $1
  then
    sed -i '' '1i\
    <!-- \
      Copyright 2021 IBM Corporation\
     \
      Licensed under the Apache License, Version 2.0 (the "License");\
      you may not use this file except in compliance with the License.\
      You may obtain a copy of the License at\
     \
          http://www.apache.org/licenses/LICENSE-2.0\
     \
      Unless required by applicable law or agreed to in writing, software\
      distributed under the License is distributed on an "AS IS" BASIS,\
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\
      See the License for the specific language governing permissions and\
      limitations under the License.\
    --> \
    ' $1
  fi
}

export -f hash_comment slash_comment css_comment html_comment

# Python
find . -type f \( -name '*.py' -o -name '*.yaml' -o -name '*.yml' -o -name '*.sh' \) -exec bash -c 'hash_comment "$0"' {} \;

# Javascript
find . -type f \( -name '*.js' -o -name '*.ts' \) -exec bash -c 'slash_comment "$0"' {} \;

# CSS
find . -type f \( -name '*.css' -o -name '*.tsx' \) -exec bash -c 'css_comment "$0"' {} \;

# HTML
find . -type f -name '*.html' -exec bash -c 'html_comment "$0"' {} \;
