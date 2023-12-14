ifndef LANG
override LANG = fa
endif
MSGDIR = jaanevis/i18n/locales/$(LANG)/LC_MESSAGES
MSGFILE = jaanevis/i18n/locales/$(LANG)/LC_MESSAGES/messages.po
MSGBASE = jaanevis/i18n/messages.pot

build-api:
	docker-compose build api

build-ui: install-ui
	npm run build --prefix jaanevis/ui

build-surge: install-ui
	npm run build-surge --prefix jaanevis/ui

install-ui:
	npm install --prefix jaanevis/ui

makemessages:
	find jaanevis -iname "*.py" | xargs xgettext -L Python --from-code=UTF-8 -o $(MSGBASE)
	sed -i -e 's/CHARSET/UTF-8/g' $(MSGBASE)
	mkdir -p $(MSGDIR)
	cp -n $(MSGBASE) $(MSGFILE)
	msgmerge --update $(MSGFILE) $(MSGBASE)

compilemessages:
	msgfmt -o $(MSGDIR)/messages.mo $(MSGFILE)

format:
	sh script/format.sh
