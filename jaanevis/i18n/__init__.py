"""configs and tools for multilingual support"""

import gettext as gettext_module
from contextvars import ContextVar

from jaanevis.config import settings

__all__ = ["set_lang_code", "get_text"]

localedir = settings.BASE_DIR / "i18n/locales"
_lang_ctx_var: ContextVar[str] = ContextVar("lang_code", default="en")


def set_lang_code(lang_code: str) -> None:
    return _lang_ctx_var.set(lang_code)


def get_lang_code() -> str:
    return _lang_ctx_var.get()


def gettext(msg: str) -> str:
    lang_code = get_lang_code()
    translation = gettext_module.translation(
        "messages", localedir, languages=[lang_code]
    )
    return translation.gettext(msg)


if __name__ == "__main__":

    def test_me():
        print(gettext("test"))
        return

    set_lang_code("fa")
    # this should print text in farsi
    test_me()

    set_lang_code("en")
    # this should be print text in english
    test_me()
