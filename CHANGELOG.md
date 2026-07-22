# CHANGELOG


## v1.0.0-alpha.4 (2026-07-22)

### Bug Fixes

- Handle missing settings gracefully in DjangoStrategy
  ([`eccba77`](https://github.com/tjarbo/pretalx-social-auth/commit/eccba777fe38f84d3f75344d90c29e3ca0400313))

Fixes #2

- Update oidc-provider-mock to latest versions
  ([`9091fa5`](https://github.com/tjarbo/pretalx-social-auth/commit/9091fa504f94fcfed2e212dba699773138f3a3ff))

### Continuous Integration

- Use main for testing the devcontainer
  ([`cab5ca7`](https://github.com/tjarbo/pretalx-social-auth/commit/cab5ca71d91d5057d212fb096768a3364edd3512))


## v1.0.0-alpha.3 (2026-05-01)

### Bug Fixes

- Resolve styling issues
  ([`5a9b577`](https://github.com/tjarbo/pretalx-social-auth/commit/5a9b577caa2c274d05ad464068ca50e4306f2151))

Co-authored-by: Copilot <copilot@github.com>


## v1.0.0-alpha.2 (2026-05-01)

### Bug Fixes

- Add missing idp parameter to enable SAML authentication
  ([`d2386f9`](https://github.com/tjarbo/pretalx-social-auth/commit/d2386f9bc1c274eecb190e226521628c99ff31dc))

Co-authored-by: Copilot <copilot@github.com>

- Resolve issues where request is a string and not a dictionary
  ([`a247b86`](https://github.com/tjarbo/pretalx-social-auth/commit/a247b86af997db8e8f3f86db6698c8fa2c11f54f))

### Chores

- Add new mock saml provider for local development
  ([`5dc4586`](https://github.com/tjarbo/pretalx-social-auth/commit/5dc4586d2b61cf9e82bce0aeee1cce33eab2a87b))

### Documentation

- Add inital version of AGENTS.md
  ([`f83a588`](https://github.com/tjarbo/pretalx-social-auth/commit/f83a588c928ef338df9065c7082941a70a137219))

- Add installation instructions
  ([`cdfea64`](https://github.com/tjarbo/pretalx-social-auth/commit/cdfea645b2a679805c7599f245fe786e69326315))

- Added troubleshooting section to CONTRIBUTING.md due to new SAML sidecar-container
  ([`5f22b6d`](https://github.com/tjarbo/pretalx-social-auth/commit/5f22b6dcebf71ed765376cbedbc145dbabaa1ecf))


## v1.0.0-alpha.1 (2026-03-24)

### Bug Fixes

- Use GITHUB_TOKEN and PyPI trusted publishing instead of secrets
  ([`2c723b4`](https://github.com/tjarbo/pretalx-social-auth/commit/2c723b44816f8d0d3dfdcc2a57c3fedade7123ba))

Co-authored-by: tjarbo <16938041+tjarbo@users.noreply.github.com>

Agent-Logs-Url:
  https://github.com/tjarbo/pretalx-social-auth/sessions/8cd93c9c-e065-4325-8f51-6e80d408ac0a

### Chores

- Add devcontainer for easier contributions
  ([`201cf13`](https://github.com/tjarbo/pretalx-social-auth/commit/201cf130b8d4c63cec650c0950663dd7fb68d3d0))

- Update devcontainer to v2
  ([`a5c1941`](https://github.com/tjarbo/pretalx-social-auth/commit/a5c19413ae423a62a8353b068cbb73cd6ce4da28))

### Documentation

- Add contribution guidelines
  ([`748ca77`](https://github.com/tjarbo/pretalx-social-auth/commit/748ca771d8776362790d4bd395ac329afb8a115a))

- Remove setup steps from CONTRIBUTING.md
  ([`048c16a`](https://github.com/tjarbo/pretalx-social-auth/commit/048c16aa3077e5c22425542a22c700932ea2d095))

Co-authored-by: tjarbo <16938041+tjarbo@users.noreply.github.com>

Agent-Logs-Url:
  https://github.com/tjarbo/pretalx-social-auth/sessions/1af11a85-4810-481a-bb88-af3af1692851

- Update project metadata, readme and license information
  ([`9e3bd9c`](https://github.com/tjarbo/pretalx-social-auth/commit/9e3bd9c0d8d4b9c597c4a9d729a935884d205311))

### Features

- Add CD pipeline using python-semantic-release
  ([`059ece0`](https://github.com/tjarbo/pretalx-social-auth/commit/059ece0ba89c728952c0262dfdedcaabc6d03872))

Co-authored-by: tjarbo <16938041+tjarbo@users.noreply.github.com>

Agent-Logs-Url:
  https://github.com/tjarbo/pretalx-social-auth/sessions/5a94d221-5ae9-48a4-9edf-fca8cacca8e6

- Allow adhoc account connection via TRUST_IDP_EMAILS setting
  ([`9b6a7b3`](https://github.com/tjarbo/pretalx-social-auth/commit/9b6a7b3a78dee7964f3a1df97d67a3f3ca6c87c6))

- Renamed plugin
  ([`4aafc68`](https://github.com/tjarbo/pretalx-social-auth/commit/4aafc686c4f447c6fc47d2167a8d59495d5f88cc))
