

SEARCHSTRING="from swagger_server.models.api_inferenceservice import ApiInferenceservice  # noqa: F401, E501"
NOQA="  # noqa: F401"

# REPLACESTRING="$SEARCHSTRING$NOQA"
REPLACESTRING="from swagger_server.models.api_inferenceservice import ApiInferenceservice  # noqa: F401, E501"

ECHO "${REPLACESTRING}"
grep -rl "${SEARCHSTRING}" ./ | LC_ALL=C xargs sed -i "" "s/${SEARCHSTRING}/${REPLACESTRING}/g"


make lint_python