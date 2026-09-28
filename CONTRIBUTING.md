# How to Contribute

## 1. Set up the environment

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) using the
version in `[tool.uv].required-version` in `pyproject.toml`, then:

```sh
uv sync --locked --python 3.14
```

This creates `.venv` and installs the SDK, test dependencies, Ruff, and Pyrefly
from `uv.lock`. Select `.venv` as the Python interpreter in VS Code and
install the recommended extensions. Use Ruff for linting and formatting and
Pyrefly for type checking.
The [Pyrefly VS Code extension](https://pyrefly.org/en/docs/IDE/#vscode-extension-settings)
uses the locked environment binary, workspace diagnostics, and inlay hints for
argument names, inferred return types, and variable types.

Python 3.11 is the minimum supported **package** version. CI tests and lints
3.11–3.14 on Linux, Windows, and macOS; development defaults to 3.14.
Development tools are defined only in the `dev` and `test`
dependency groups and installed from `uv.lock`.

## 2. Run checks

```sh
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked pyrefly check
uv run --locked pytest
uv build
```

Tests use mocked HTTP responses; no live tenant or API key is needed. Pytest
discovers `Test*.py` files and writes JUnit XML, terminal coverage, `coverage.xml`
(Cobertura), and `htmlcov/`. Branch coverage is enabled; generated version code
is excluded.

To check compatibility on an older supported interpreter (including polyfills
and syntax/type compatibility), switch interpreters and run the same checks as CI:

```sh
uv sync --locked --python 3.11
uv run --no-sync ruff check --target-version py311 .
uv run --no-sync ruff format --check --target-version py311 .
uv run --no-sync pyrefly check --python-version 3.11
uv run --no-sync pytest
```

Repeat with 3.12 and 3.13 (and matching Ruff/Pyrefly flags); don't assume that
passing checks on 3.14 guarantees compatibility with earlier supported versions.
Run `uv sync --locked --python 3.14` to restore the development environment.
To update dependencies intentionally, use `uv lock --upgrade` (or
`uv lock --upgrade-package NAME`) and commit the resulting lockfile with any
`pyproject.toml` changes. Tool upgrades must also update their pinned constraints.

## 3. Formatting and typing

Use Ruff's format-on-save integration or `uv run ruff format PATH` for edited
Python files. CI enforces formatting and linting for SDK source and tests;
samples remain excluded. Explicit `Any` is limited to the JSON wire-schema
compiler's runtime annotations and the test decorators' dynamic unittest instances.

`uv run --locked pyrefly check` checks the SDK and tests on the development Python
version without a diagnostic baseline. CI also checks each supported version.
Keep annotations accurate without
changing public method names, parameters, or runtime behavior.
Use `TypeVar` and `Generic[T]` for generic classes until the minimum supported
Python is 3.12; PEP 695's `class Name[T]` syntax cannot be parsed by Python 3.11.
DTOs use PEP 604 `T | None` annotations; the msgspec wire-schema compiler
resolves them on every supported Python version.
Unknown responses use `object` rather than `Any`, and nullable service results
include `None`. Preserve public import paths and wire formats when
changing internal typing.

## 3.1 JSON wire format

`Artesian._ClientsExecutor.ArtesianJsonSerializer` maps DTO dataclasses to the
Artesian JSON wire format with msgspec: PascalCase keys, omitted `None` fields,
enums by name, and RFC 3339 datetimes (naive stays naive, UTC ends in `Z`,
zero microseconds are omitted). A `dict` field is sent as a JSON object unless
it is declared with `keyValueArrayField()`, which sends it (and every dict
nested in it) as `[{"Key": k, "Value": v}]`. Decoding into any `dict` accepts
both shapes. `benchmark/bench_serde.py` measures large payloads; see
`benchmark/README.md`.

## 4. CI and coverage

The OS/Python matrix builds the package and runs Ruff, Pyrefly, and pytest for
every event. The single **Checks** job is the required PR check: it combines
coverage data, publishes test results, HTML/XML artifacts and a job summary,
and fails if the matrix or reporting fails. Native GitHub coverage uses a
job-scoped `code-quality: write` permission. PR checks run on GitHub's merge
commit; pushes to `master` establish the comparison baseline. Fork PRs still
run tests and produce coverage artifacts/summaries, but skip uploads
requiring write access. Preview tags use the same matrix and report their
tagged commit.

## 5. Release tags

Use a `v` prefix and canonical, unpadded numeric components. The package
version on PyPI is the tag without `v`; no version remapping is performed.

- **Stable:** `vX.Y.Z` (for example, `v4.3.0`). The tagged commit must be
  contained in `master`.
- **Beta:** `vX.Y.ZbN` (for example, `v4.3.0b1` or `v5.0.0b1`). The tagged
  commit must be contained in `develop-beta`. Compared with the latest stable
  tag on `master`, the base version must be either the next minor
  (`X.(Y+1).0`) or the next major (`(X+1).0.0`).
- **PR preview:** `vX.Y.ZaPR.postITER` (for example, `v4.3.0a69.post2`).
  `X.Y.Z` must match the latest stable tag on `master`; `PR` is the pull
  request number and `ITER` is the preview iteration. The tag must point
  to that PR's current, unmerged head commit, which must contain current
  `master`—not GitHub's synthetic PR merge commit.

Only a pushed release tag or a manual workflow dispatch **on a tag ref** can
build a release and publish, after the matrix and **Checks** job pass. The
release build verifies that the remote tag still points at the checked-out
commit. PRs and branch dispatches cannot publish. The protected publisher
checks that the wheel and sdist filenames match the release tag before upload;
review the build source SHA and distribution hashes before approving it.
