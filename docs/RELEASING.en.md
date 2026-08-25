# Release guide

[简体中文](RELEASING.md)

The project publishes through GitHub Actions and PyPI Trusted Publishing (OIDC). The build job has
no publishing permission, while the publishing job receives only distributions that have already
been tested and checked. No PyPI API token is stored in the repository or GitHub Secrets.

## Initial setup

Project administrators perform these steps once.

1. Create an environment named `pypi` under **Settings → Environments** in the GitHub repository.
2. Add required reviewers to `pypi` and restrict deployment tags to `v*`.
3. Add a GitHub Trusted Publisher under **Manage → Publishing** for the PyPI project
   `chinese-address-generator`:

   | Field | Value |
   | --- | --- |
   | Owner | `Ginkgoty` |
   | Repository | `chinese-address-generator` |
   | Workflow name | `release.yml` |
   | Environment name | `pypi` |

The workflow filename and environment name registered on PyPI must exactly match
`.github/workflows/release.yml`.

## Publishing a release

1. Change only `__version__` in `chinese_address_generator/_version.py`. The build backend reads the
   version from this file, so there is no second version value to synchronise.
2. Replace `Unreleased` for that version in `CHANGELOG.md` with the release date.
3. Run the complete local verification suite:

   ```bash
   uv lock --check
   uv run ruff check .
   uv run ruff format --check .
   uv run pytest
   uv build
   uv run twine check dist/*
   ```

4. Review all changes. Create a GPG-signed commit only after the maintainer gives explicit approval;
   never commit without that approval.
5. Create and push a signed tag for the same version, for example:

   ```bash
   git tag -s v1.0.0 -m "Release 1.0.0"
   git push origin main
   git push origin v1.0.0
   ```

6. Create a GitHub Release from that tag. Only **Publish release** triggers the release workflow;
   saving a draft does not upload anything to PyPI.
7. Inspect the tests and distributions from the `build` job, then have an authorised maintainer
   approve deployment to the `pypi` environment.
8. Confirm that the version, wheel, source distribution, and digital attestations appear on PyPI.

The workflow rejects tags that do not start with `v`, as well as releases whose tag and package
versions differ.

## Handling failures

PyPI does not allow files for a version to be overwritten. A workflow that fails before uploading
may be fixed and rerun. If any distribution has already been uploaded, publish a new version rather
than deleting and reusing the old version number. Do not enable `skip-existing` for production
releases, because it can conceal an incomplete release.
