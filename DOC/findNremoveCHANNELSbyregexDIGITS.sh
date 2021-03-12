#!/bin/bash
# License MIT
find . -name '[[:digit:]]*.cgi' -print -exec rm -v {} \;
