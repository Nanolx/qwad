#!/bin/sh
#makeqwaddeb#
VERSION=$1
Sources=$(find | grep -v pyc$ | grep -v ui$ | grep -v ts$ | grep -v .pro$ | grep -v .qrc$ | grep -v bz2$ | grep -v dist | grep -v -w icons | grep -v ~$ | grep -v examinar | grep -v e4.$ | grep -v eric | grep -v  makeqwaddeb)

cp -r GUI dist_debian/usr/share/Qwad/
cp -r wii_signer dist_debian/usr/share/Qwad/
cp -r  i18n dist_debian/usr/share/Qwad/
cp Qwad.pyw dist_debian/usr/share/Qwad/
cp Qwad_rc.py dist_debian/usr/share/Qwad/
cp README.txt dist_debian/usr/share/Qwad/
cp CHANGELOG.txt dist_debian/usr/share/Qwad/



kwrite dist_debian/DEBIAN/control
rm dist_debian/DEBIAN/control~

dpkg --build dist_debian/ qwad-"$VERSION"_all.deb
