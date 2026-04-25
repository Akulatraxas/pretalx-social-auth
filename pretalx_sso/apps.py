from django.apps import AppConfig
from django.utils.translation import gettext_lazy

from . import __version__


class PluginApp(AppConfig):
    name = "pretalx_sso"
    verbose_name = "Single Sign-On for pretalx"

    class PretalxPluginMeta:
        name = gettext_lazy("Single Sign-On for pretalx")
        author = "Tjark <tjarbo/>"
        description = gettext_lazy(
            "Enable Single Sign-On capabilities on your pretalx instance."
        )
        visible = True
        version = __version__
        category = "INTEGRATION"

    def ready(self):
        from . import signals  # NOQA
