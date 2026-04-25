from urllib.parse import urlencode

from django.dispatch import receiver
from django.template.loader import get_template
from django.urls import reverse
from pretalx.common.signals import auth_html, profile_bottom_html
from pretalx.orga.signals import nav_event_settings
from pretalx.person.signals import delete_user

from .utils import all_backends, backend_friendly_name, load_strategy, user_backends


@receiver(nav_event_settings)
def pretalx_sso_settings(sender, request, **kwargs):
    if not request.user.has_perm("orga.change_settings", request.event):
        return []
    return [
        {
            "label": "pretalx Social Auth plugin",
            "url": reverse(
                "plugins:pretalx_sso:settings",
                kwargs={"event": request.event.slug},
            ),
            "active": request.resolver_match.url_name
            == "plugins:pretalx_sso:settings",
        }
    ]


@receiver(auth_html)
def render_login_auth_options(sender, request, next_url=None, **kwargs):
    context = {"backend_options": []}

    request_obj = request if hasattr(request, "GET") else kwargs.get("request")
    next_path = next_url
    if request_obj and hasattr(request_obj, "GET"):
        next_path = request_obj.GET.get("next", next_url)
    elif isinstance(request, str) and request:
        next_path = request

    saml_idps = load_strategy().get_setting("SOCIAL_AUTH_SAML_ENABLED_IDPS") or {}
    for class_name, be_class in all_backends().items():
        friendly_name = backend_friendly_name(be_class)

        if class_name == "saml" and isinstance(saml_idps, dict) and saml_idps:
            for idp_name, idp_settings in saml_idps.items():
                idp_label = idp_name
                if isinstance(idp_settings, dict):
                    idp_label = idp_settings.get("name") or idp_settings.get("entity_id") or idp_name

                params = {"idp": idp_name}
                if next_path:
                    params["next"] = next_path

                context["backend_options"].append(
                    {
                        "backend": class_name,
                        "label": friendly_name if len(saml_idps) == 1 else f"{friendly_name} ({idp_label})",
                        "url_params": f"?{urlencode(params)}",
                    }
                )
            continue

        params = {}
        if next_path:
            params["next"] = next_path
        context["backend_options"].append(
            {
                "backend": class_name,
                "label": friendly_name,
                "url_params": f"?{urlencode(params)}" if params else "",
            }
        )

    template = get_template("pretalx_sso/login.html")
    html = template.render(context=context, request=request_obj)
    return html


@receiver(profile_bottom_html)
def render_user_options_backends(sender, user, **kwargs):
    user_backend_data = user_backends(user)
    context = {}
    context["associated_accounts"] = [
        (backend_friendly_name(assoc.provider), assoc)
        for assoc in user_backend_data["associated"]
    ]
    template = get_template("pretalx_sso/profile_settings.html")
    html = template.render(context=context)
    return html


@receiver(delete_user)
def delete_user_data(sender, user, **kwargs):
    user.social_auth.all().delete()
