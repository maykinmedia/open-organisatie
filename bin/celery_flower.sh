#!/bin/bash
exec celery --app openorganisatie --workdir src flower
