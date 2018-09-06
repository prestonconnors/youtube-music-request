#!/bin/bash

DIR="$1"

. "${DIR}/venv/bin/activate"
"${DIR}/venv/bin/gunicorn" --chdir "${DIR}" -D -c "${DIR}/gunicorn.conf" main:APP