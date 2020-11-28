#!/bin/bash

ENTRYPOINT="$*"

if [ -z "$ENTRYPOINT" ]; then
    python /src/app.py
else
    /bin/sh -c "$ENTRYPOINT"
fi
