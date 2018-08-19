#!/bin/sh
set -eo pipefail
shopt -s nullglob

supervisord -c ~/supervisord.conf
supervisorctl start wxchat

exec "$@"