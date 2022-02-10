#!/usr/bin/env bash

set -e

python3 -m venv venv

export PATH=venv/bin:${PATH}

pip install -r requirements-dev.txt