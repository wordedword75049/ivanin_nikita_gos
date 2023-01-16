#!/bin/bash

set -eu

if [ -z "$1" ]
then
  echo "You must specify argument: 'frontend' or 'backend'"
fi

if [ "$1" == frontend ]
then
  npm run-script start-docker
fi

if [ "$1" == backend ]
then
  gunicorn --bind 0.0.0.0:5000 app:app
fi
