"""configs and tools for multilingual support"""

import builtins
import gettext
from contextlib import contextmanager
from functools import partial

from jaanevis.config import settings

__all__ = ["t_", "translate"]


localedir = settings.BASE_DIR / "i18n/locales"
translate_en = gettext.translation(
    "messages", localedir, fallback=False, languages=["en"]
)
translate_fa = gettext.translation(
    "messages", localedir, fallback=False, languages=["fa"]
)
translations = {
    "en": translate_en,
    "fa": translate_fa,
}
translate_en.install()


def t_(msg: str, lang: str = settings.LANGUAGE_CODE) -> str:
    return translations.get(lang, translations["en"]).gettext(msg)


@contextmanager
def translate(lang: str = "en"):
    """temporarily replace global gettext (_) function to custom t_ function with language choice"""
    org_func = builtins.__dict__["_"]
    new_func = partial(t_, lang=lang)
    builtins.__dict__["_"] = new_func
    yield
    builtins.__dict__["_"] = org_func


if __name__ == "__main__":

    def test_me():
        print(_("test"))
        return

    with translate("fa"):
        # this should print text in farsi
        test_me()
    # this should be print text in english
    test_me()
