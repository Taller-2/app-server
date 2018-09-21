#!/usr/bin/env sh

python -m pytest --cov=server SKIP_AUTH=YES
