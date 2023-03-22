#!/usr/bin/env bash
ps -ef | grep 'AppAlertingBackend.asgi:application' | grep -v grep | awk '{print $2}' | xargs kill
echo stopped