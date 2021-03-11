#!/bin/bash
# (c) 2021-01-12 Kelsie Flynn
# License MIT
find . -name '[[:digit:]]*.cgi' -print -exec rm -v {} \;
