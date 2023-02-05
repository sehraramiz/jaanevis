Some related notes on some related locations around the world


### translations

0- install [gnu gettext](https://www.gnu.org/software/gettext/) to access msgfmt, xgettext,  msgmerge tools


1- create/update language .po file
```bash
make LANG=fa makemessages
```

2- translate messages in ```jaanevis/i18n/locales/fa/LC_MESSAGES/messages.po```

3- compile translation to .mo file
```bash
make LANG=fa compilemessages
```
