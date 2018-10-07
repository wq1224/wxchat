#!/bin/bash
set -e
shopt -s nullglob

supervisord -c ~/supervisord.conf

exec "$@"