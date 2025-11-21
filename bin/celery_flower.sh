#!/bin/bash

# Set defaults for OTEL
export OTEL_SERVICE_NAME="${OTEL_SERVICE_NAME:-openorganisatie-flower}"

exec celery --app openorganisatie --workdir src flower
