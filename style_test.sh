#!/usr/bin/env bash
# E501 Line too long
# E265 block comment should start with '# '
pycodestyle *.py modules/* --ignore=E501,E265
