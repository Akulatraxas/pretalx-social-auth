#!/bin/sh
# Plugin specific post-create.sh script.
set -e

# Install system dependencies
sudo apt-get update && sudo apt-get install -y gettext

# Install required runtime dependency for social_core SAML backend.
pip3 install --upgrade python3-saml

# Install development dependencies for style checks
pip3 install --upgrade isort flake8 flake8-bugbear black djhtml twine check-manifest build
