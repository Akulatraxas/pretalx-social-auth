#!/bin/sh
# Plugin specific post-create.sh script.
set -e

# Install required runtime dependency for social_core SAML backend.
pip3 install --upgrade python3-saml
