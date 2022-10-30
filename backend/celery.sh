#!/bin/bash
cd /app
/opt/venv/bin/celery -A config.celery worker --pool=solo -l info 