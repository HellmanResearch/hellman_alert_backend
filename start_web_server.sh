#!/usr/bin/env bash
nohup ../venv/bin/daphne AppAlertingBackend.asgi:application -b 0.0.0.0 -p 8011 >> web_server_stdout.log 2>&1 &
echo started