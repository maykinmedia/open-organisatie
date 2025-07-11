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
    --urlconf openorganisatie.scim.api.urls \
    --file src/openorganisatie/scim/scim-openapi.yaml \
    --custom-settings openorganisatie.scim.api.urls.custom_settings