"""
Custom pipeline functions for pretalx social auth plugin.
"""

import logging

from django.contrib.auth import get_user_model
from social_core.exceptions import AuthForbidden

logger = logging.getLogger(__name__)


def associate_by_email_if_trusted(
    strategy, details, backend, user=None, *args, **kwargs
):
    """
    Pipeline function to handle email-based account association.

    This function checks if a user is logging in via SSO for the first time,
    and if a user with the same email already exists in the database.

    The global TRUST_IDP_EMAILS setting controls whether existing accounts
    should be automatically linked. If disabled (default), the login will be rejected.

    This should be placed in the pipeline BEFORE the 'social_core.pipeline.user.create_user' step.
    """
    if user:
        # User is already associated or logged in, skip this check
        return

    # Get email from details
    email = details.get("email")
    if not email:
        # No email provided by the IDP, can't do email matching
        return

    # Check if a user with this email already exists
    User = get_user_model()
    email_field = getattr(User, "EMAIL_FIELD", "email")
    existing_users = User._default_manager.filter(**{email_field + "__iexact": email})

    if not existing_users.exists():
        # No existing user with this email, proceed with normal flow
        return

    # There is an existing user with this email
    # Check the global TRUST_IDP_EMAILS setting (default: False for security)
    # strategy.get_setting() returns None if not configured, so we default to False
    trust_idp_emails = strategy.get_setting("TRUST_IDP_EMAILS")
    if trust_idp_emails is None:
        trust_idp_emails = False

    if not trust_idp_emails:
        # Trust is not enabled, reject the login
        raise AuthForbidden(
            backend,
            f"An account with email {email} already exists. "
            "Please log in with your existing credentials first, "
            "then connect your social account from your profile settings.",
        )

    # Trust is enabled, return the existing user to associate with this social auth
    existing_user = existing_users.first()
    return {"user": existing_user, "is_new": False}


def sync_teams_from_idp(
    strategy, details, response, user=None, social=None, *args, **kwargs
):
    """
    Pipeline function to sync IDP group memberships to pretalx Team memberships.

    Reads the user's group list from the OIDC response and maps them to pretalx
    Team objects via the IDP_GROUP_TO_PRETALX_TEAM setting (a dict mapping IDP
    group identifiers to pretalx Team primary keys).

    This is add-only: users are added to teams but never removed. Removal
    support can be added as an opt-in feature later.

    The raw IDP groups list is stored in UserSocialAuth.extra_data["idp_groups"]
    for auditing and debugging purposes.

    This should be placed in the pipeline AFTER 'social_core.pipeline.user.user_details'
    so the user object is fully created and associated.
    """
    if not user:
        return

    # Read the claim key (default: "groups") and the mapping config
    try:
        claim_key = strategy.get_setting("IDP_GROUPS_CLAIM_KEY")
    except AttributeError:
        claim_key = "groups"

    try:
        group_to_team_mapping = strategy.get_setting("IDP_GROUP_TO_PRETALX_TEAM")
    except AttributeError:
        group_to_team_mapping = {}

    if not isinstance(group_to_team_mapping, dict) or not group_to_team_mapping:
        # No mapping configured — nothing to do
        return

    # Extract groups from the OIDC response
    idp_groups = response.get(claim_key, []) if response else []

    if not isinstance(idp_groups, list):
        logger.warning(
            "IDP groups claim '%s' is not a list (got %s), skipping team sync",
            claim_key,
            type(idp_groups).__name__,
        )
        return

    # Store raw IDP groups in extra_data for auditing
    if social is not None:
        extra_data = social.extra_data or {}
        extra_data["idp_groups"] = idp_groups
        social.set_extra_data(extra_data)

    # Lazy import to avoid circular imports at module load time; this model
    # is always available when the plugin runs inside pretalx.
    from pretalx.event.models import Team

    # Sync: add user to mapped teams
    for idp_group in idp_groups:
        team_id = group_to_team_mapping.get(idp_group)
        if team_id is None:
            # This IDP group has no mapping configured — skip silently
            continue

        try:
            team_id = int(team_id)
        except (ValueError, TypeError):
            logger.warning(
                "Invalid team ID '%s' for IDP group '%s', skipping",
                team_id,
                idp_group,
            )
            continue

        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            logger.warning(
                "Pretalx Team with ID %d not found (mapped from IDP group '%s'), skipping",
                team_id,
                idp_group,
            )
            continue

        if not team.members.filter(pk=user.pk).exists():
            team.members.add(user)
            logger.info(
                "Added user '%s' to pretalx Team '%s' (ID %d) via IDP group '%s'",
                user,
                team.name,
                team_id,
                idp_group,
            )

