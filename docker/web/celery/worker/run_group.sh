#!/bin/bash

set -euo pipefail

# DEBUG set in .env_docker_compose
if [ ${DEBUG:-0} = 1 ]; then
    log_level="debug"
else
    log_level="info"
fi

if [ ${DJANGO_SETTINGS_MODULE} = "config.settings.production" ]; then
  export DJANGO_SETTINGS_MODULE="config.settings.production_celery"
fi

sleep 1  # Wait for migrations
echo "==> $(date +%H:%M:%S) ==> Running Celery worker <=="
echo "==> $(date +%H:%M:%S) ==> Celery worker watch queue: ${CELERY_WATCH_QUEUE}"
exec celery -A config.celery_app worker --loglevel $log_level --pool=gevent --autoscale=120,80 -Q ${CELERY_WATCH_QUEUE}
