# How to Contribute

## 1. Set up the environment

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) using the
version in `[tool.uv].required-version` in `pyproject.toml`, then:

```sh
uv sync --locked --python 3.12
```

This creates `.venv` and installs the SDK, test dependencies, Ruff, Pyrefly, and
Twine from `uv.lock`. Select `.venv` as the Python interpreter in VS Code and
install the recommended extensions. Pyrefly replaces Pylance/Pyright; Ruff
replaces Black and Flake8. Pyrefly is a type checker, not a formatter.
The [Pyrefly VS Code extension](https://pyrefly.org/en/docs/IDE/#vscode-extension-settings)
uses the locked environment binary, workspace diagnostics, and inlay hints for
argument names, inferred return types, and variable types.

Python 3.10 is the minimum supported **package** version. CI tests 3.10–3.14
on Linux, Windows, and macOS; quality checks run on 3.12 for a consistent typing
environment. Development tools are defined only in the `dev` and `test`
dependency groups and installed from `uv.lock`; the legacy `.[dev]` extra
has been removed. Use `uv sync` instead.

End-of-life Python 3.8/3.9 are no longer supported.

## 2. Run checks

```sh
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked pyrefly check
uv run --locked pytest
uv build
uv run --locked twine check dist/*
```

Tests use mocked HTTP responses; no live tenant or API key is needed. Pytest
discovers `Test*.py` files and writes JUnit XML, terminal coverage, `coverage.xml`
(Cobertura), and `htmlcov/`. Branch coverage is enabled; generated version code
is excluded.

To check the minimum supported interpreter without installing development tools:

```sh
uv sync --locked --python 3.10 --no-dev --group test
uv run --no-sync pytest
```

Run `uv sync --locked --python 3.12` to restore the development environment.
To update dependencies intentionally, use `uv lock --upgrade` (or
`uv lock --upgrade-package NAME`) and commit the resulting lockfile with any
`pyproject.toml` changes. Tool upgrades must also update their pinned constraints.

## 3. Formatting and typing

Use Ruff's format-on-save integration or `uv run ruff format PATH` for edited
Python files. CI enforces formatting and linting for SDK source; tests and
samples retain their existing exclusion from lint checks. Explicit `Any` is
allowed only in the jsons adapter, which forwards dynamic plugin keyword arguments.

`uv run --locked pyrefly check` checks the SDK against the minimum supported
Python version without a diagnostic baseline. Keep annotations accurate without
changing public method names, parameters, or runtime behavior.
Consumer typing may become stricter: unknown responses use `object` rather than
`Any`, and nullable service results include `None`. Public import paths remain
unchanged; internal typing cleanup must preserve jsons wire formats.

## 4. GitHub coverage

Enable **Code Quality** in the repository's GitHub settings to use native
[code coverage](https://docs.github.com/en/code-security/how-tos/maintain-quality-code/set-up-code-coverage).
No third-party coverage account or token is required.

CI combines raw coverage data from the Python/OS matrix, publishes HTML/XML
artifacts and a job summary, then uses `actions/upload-code-coverage` with a
job-scoped `code-quality: write` permission. PR coverage uses the PR head commit;
pushes to `master` establish the comparison baseline. Fork PRs still run tests
and produce coverage artifacts/summaries, but skip uploads requiring write
access. Tag previews retain separate reports because they test a different
merged commit.

## 5. Release setup (maintainers)

Before enabling production publishing, complete these manual prerequisites:

- An owner of the PyPI project **`artesian-sdk`** must register a Trusted
  Publisher with owner **`ARKlab`**, repository **`Artesian.SDK-Python`**, workflow
  filename **`python-tests.yml`**, and environment **`pypi`**, matching exactly.
- Protect the GitHub **`pypi`** environment with required reviewers, prevent
  self-review, and restrict deployment to the repository's release tag patterns.
  Organization policy must allow the pinned, early-stage
  `astral-sh/attest-action` v0.0.6
  (`f589a42a7efb6fe400b4f400de60b4bc90390027`) and network access to Sigstore,
  GitHub OIDC, and PyPI.
- Rehearse on TestPyPI using a separate project, Trusted Publisher, and protected
  environment before production. A separately reviewed rehearsal workflow must
  configure **both** the upload destination and its Integrity API verification
  endpoint, and change the verifier's expected publisher environment (currently
  literal `pypi`) to match the rehearsal environment. Changing only the upload
  URL is insufficient.

Release builds retain `uv build` and Twine metadata checks in `build-stable`,
`build-beta`, and `build-preview`, without OIDC permission. Stable releases
retain the `master` source rule, beta releases `develop-beta`, and previews
merge the PR into current `master`, normalizing versions to `X.Y.ZaPR.postITER`.
The preview build's merge SHA differs from the triggering tag/workflow SHA.

The separate `publish` job uses environment `pypi` and only `contents: read`
and `id-token: write` permissions. It downloads wheel/sdist artifacts by
immutable Actions artifact ID; it does not check out or build source, or
install packages from those artifacts. Summaries record the actual build source
SHA, artifact SHA256 digests, and workflow run identity. **Reviewers must inspect
that build source and those digests before approving the environment**, especially
for previews; reviewing the triggering tag alone is insufficient.

The pinned attestation action creates PEP 740 `.publish.attestation` sidecars;
uv **0.12.19** uploads with `--trusted-publishing always`. Explicit checks require
sidecars before upload and confirm post-upload PyPI Integrity API attestation
presence, subject digests, and publisher identity over HTTPS. This is a
consistency/presence check, **not independent cryptographic verification**;
PyPI verifies signatures on upload. These attestations establish publication
identity, **not full build provenance**. A post-upload check failure cannot roll
back published files. Retrying an identical file may skip its upload, so missing
attestations require investigation rather than assuming a retry will repair them.

This repository change does not perform external administrative setup or publish
to production. Revoke `PYPI_API_TOKEN` only after a successful migration,
verification checks, and confirmation that no other consumers need it; its
revocation is a separate maintainer action.
