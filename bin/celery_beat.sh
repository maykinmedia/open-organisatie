#!/bin/bash

set -e

LOGLEVEL=${CELERY_LOGLEVEL:-INFO}

# Set defaults for OTEL
export OTEL_SERVICE_NAME="${OTEL_SERVICE_NAME:-openorganisatie-scheduler}"

mkdir -p celerybeat

echo "Starting celery beat"
exec celery --workdir src --app openorganisatie beat \
    -l $LOGLEVEL \
    -s ../celerybeat/beat
