#!/usr/bin/env bash

set -e

export PATH=venv/bin:${PATH}

flake8 src/ demo/