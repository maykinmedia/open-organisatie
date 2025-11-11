#!/bin/sh
#
# Generate the API schema from the code into the output file.
#
# Run this script from the root of the repository:
#
#   ./bin/generate_api_schema.sh
#

src/manage.py spectacular \
    --validate \
    --fail-on-warn \
    --lang=nl \
    --urlconf openorganisatie.identiteit.api.urls \
    --file src/identiteit-openapi.yaml \
    --custom-settings openorganisatie.identiteit.api.urls.custom_settings

src/manage.py spectacular \
    --validate \
    --fail-on-warn \
    --lang=nl \
    --urlconf openorganisatie.organisatie.api.urls \
    --file src/organisatie-openapi.yaml \
    --custom-settings openorganisatie.organisatie.api.urls.custom_settings