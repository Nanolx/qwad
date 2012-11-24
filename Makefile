all:
	-lrelease i18n/Qwad_de.ts

clean:
	rm -rf GUI/__pycache__/
	rm -f *.pyc
	rm -f **/*.pyc

install:
	mkdir -p $(DESTDIR)/usr/share/Qwad/i18n
	mkdir -p $(DESTDIR)/usr/bin
	install -m755 qwad $(DESTDIR)/usr/bin
	install -m644 i18n/*.qm $(DESTDIR)/usr/share/Qwad/i18n
	cp -r GUI WiiPy TitleIDs.py Qwad.pyw Qwad_rc.py icons README COPYING AUTHORS $(DESTDIR)/usr/share/Qwad/

uninstall:
	rm -f $(DESTDIR)/usr/bin/qwad
	rm -rf $(DESTDIR)/usr/share/Qwad/

update-trans:
	pylupdate4 Qwad.pro
	mv *.ts i18n/
	sed -e 's,filename=\",filename=\"../,g' -i i18n/*.ts
