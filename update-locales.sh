#!/bin/bash

# Update .po files
find locale -name "*.po" -execdir xgettext -L Python -j -o synclient-tools.po --package-name synclient-tools --package-version 0.2 --msgid-bugs-address paskao@hacari.org `pwd`/synclient-tools \;
find locale -name "*.po" -execdir msgfmt synclient-tools.po -o synclient-tools.mo \;

