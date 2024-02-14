#!/bin/bash

# start celery worker
celery -A config worker -l INFO &

# start celery beat
celery -A config beat -l INFO -S django &

tail -f /dev/null
