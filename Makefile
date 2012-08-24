all:

clean:
	rm -fv **/*.pyc

install:
	mkdir -p $(DESTDIR)/usr/share/Qwad/i18n
	mkdir -p $(DESTDIR)/usr/bin
	install -m755 qwad $(DESTDIR)/usr/bin
	install -m644 i18n/*.ts $(DESTDIR)/usr/share/Qwad/i18n
	cp -r GUI i18n Qwad.pyw Qwad_rc.py README COPYING AUTHORS $(DESTDIR)/usr/share/Qwad/

uninstall:
	rm -f $(DESTDIR)/usr/bin/qwad
	rm -rf $(DESTDIR)/usr/share/Qwad/

update-trans:
	pylupdate4 Qwad.pro
	mv *.ts i18n/
	sed -e 's,filename=\",filename=\"../,g' -i i18n/*.ts
