# Contributing

Every contribution is highly welcome! This document describes contribution guidelines, how to setup your environment, specific to the plugin development. Please get familiar with the [general pretalx-plugin documentation](https://docs.pretalx.org/developer/plugins/).

## General Guidelines

* **DO** give priority to the current style of the project or file you're changing even if it diverges from the general guidelines.
* **DO** submit all code changes via pull requests (PRs) rather than through a direct commit. PRs will be reviewed and potentially merged by the repo maintainers after a peer review that includes at least one maintainer.
* **DO** refer to any relevant issues, and include keywords that automatically close issues when the PR is merged.
* **DO** address PR feedback in an additional commit(s) rather than amending the existing commits, and only rebase/squash them when necessary. This makes it easier for reviewers to track changes.
* **DO** assume that "Squash and Merge" will be used to merge your commit unless you request otherwise in the PR.
* **DO** NOT fix merge conflicts using a merge commit. Prefer `git rebase`.
* **DO** NOT mix independent, unrelated changes in one PR. Separate real product/test code changes from larger code formatting/dead code removal changes. Separate unrelated fixes into separate PRs, especially if they are in different assemblies.

## Merging Pull Requests

* **DO** use "Squash and Merge" by default for individual contributions unless requested by the PR author. Do so, even if the PR contains only one commit. It creates a simpler history than "Create a Merge Commit".

# How to setup your local environment

This project leverages the [Development Containers](https://containers.dev/) technology to ensure a reliable and simple setup for contributors. Please ensure that your IDE or editor like Visual Studio Code is preapred to use `.devcontainers` and that you have a container engine like podman installed. Just reopen the project in your development container and you ready to code.

In case you do not use devcontainers, we here is a small setup code, just in case:

1. Make sure that you have a working [pretalx development setup](https://docs.pretalx.org/en/latest/developer/setup.html).
2. Clone this repository, eg to `local/pretalx-social-auth`.
3. Activate the virtual environment you use for pretalx development.
4. Run `pip install -e .` within this directory to register this application with pretalx's plugin registry.
5. Run `make` within this directory to compile translations.
6. Restart your local pretalx server. This plugin should show up in the plugin list shown on startup in the console. You can now use the plugin from this repository for your events by enabling it in the 'plugins' tab in the settings.

## First steps

After your environment is ready, please follow these to little steps to start coding:

* Use `python3 -m pretalx runserver` to start a development server which automatically uses this plugin.
* You need to login first via username and password, as plugins are disabled by default in pretalx. Go to [`/orga/event/democon/settings/plugins`](http://localhost:8000/orga/event/democon/settings/plugins#tab-INTEGRATION) and enable the plugin.
  * Username: superuser@pretalx.local
  * Password: pretalx
* An fake IDP is listening on port [`:9400`](http://localhost:9400) and is configured to be used via OIDC.

## Releasing

This project uses [python-semantic-release](https://python-semantic-release.readthedocs.io/) and [Conventional Commits](https://www.conventionalcommits.org/) to automate versioning and publishing. **You do not need to manually bump versions or create tags.**

### Branch strategy

| Branch    | What happens on push                                                                      |
|-----------|-------------------------------------------------------------------------------------------|
| `main`    | A pre-release is created and published to PyPI (e.g. `1.2.0-alpha.1`).                   |
| `release` | A stable release is created and published to PyPI (e.g. `1.2.0`).                        |

### How a release is made

1. **Merge to `main`** – the CD pipeline runs `python-semantic-release`, which inspects commit messages since the last release, determines the next version following [semver](https://semver.org/), commits the version bump, creates a Git tag, publishes a GitHub Release, and uploads the built package to PyPI as a **pre-release**.
2. **Promote to `release`** – once the pre-release has been tested and approved, merge `main` into the `release` branch. The same pipeline runs again and publishes the same version as a **stable release** on PyPI.

### Commit message format

Semantic release determines the version bump from commit messages. Use the following prefixes:

| Prefix            | Version bump | Example                                      |
|-------------------|-------------|----------------------------------------------|
| `fix:`            | Patch        | `fix: handle missing config key gracefully`  |
| `feat:`           | Minor        | `feat: add GitHub OAuth backend support`     |
| `feat!:` / `BREAKING CHANGE:` | Major        | `feat!: remove deprecated pipeline hook` |
| `chore:`, `docs:`, `style:`, `refactor:`, `test:` | None | `docs: update README` |

## Checks

This plugin has CI set up to enforce a few code style rules. To check locally, you need these packages installed::

    pip install flake8 flake8-bugbear isort black djhtml

To check your plugin for rule violations, run::

    black --check .
    isort -c .
    djhtml -c .
    flake8 .

You can auto-fix some of these issues by running::

    isort .
    black .
    djhtml .

## Troubleshooting

## Rebuilding the DevContainer fails.

As all containers in this project share the same network stack, the have to be stopped and removed in a certain order. Otherwise, your container engine might fail to rebuild the DevContainer with an error like ` Error: container <container_1> has dependent containers which must be removed before it: <container_2>, <container_3>: container already exists`.

Please delete stop and remove in this case the containers manually, `saml-provider-mock` and `oidc-provider-mock` before you stop and remove `devcontainer`.
