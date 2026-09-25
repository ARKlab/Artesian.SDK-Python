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

Python 3.8 remains the minimum supported **package** version. CI tests 3.8–3.14
on Linux, Windows, and macOS; quality checks run on 3.12 for a consistent typing
environment. The legacy `pip install -e '.[dev]'` extra remains available,
but uv dependency groups and the lockfile are the canonical development setup.

Python 3.8/3.9 are end-of-life. Their compatible urllib3 releases, and the
cryptography release used by older development tooling, have known advisories
whose fixes require newer Python. Use a maintained interpreter for development
and production; retaining the package's existing Python floor does not make
those legacy dependency combinations secure.

## 2. Run checks

```sh
uv run --locked ruff check .
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
uv sync --locked --python 3.8 --no-dev --group test
uv run --no-sync pytest
```

Run `uv sync --locked --python 3.12` to restore the development environment.
To update dependencies intentionally, use `uv lock --upgrade` (or
`uv lock --upgrade-package NAME`) and commit the resulting lockfile with any
`pyproject.toml` changes. Tool upgrades must also update their pinned constraints.

## 3. Formatting and typing

Use Ruff's format-on-save integration or `uv run ruff format PATH` for edited
Python files. Repository-wide format enforcement is deferred to a separate
formatting-only change to avoid rewriting SDK code in this tooling migration.
Linting retains the existing source-only scope and selected legacy style rules.

`pyrefly-baseline.json` records existing diagnostics without changing public
annotations or behavior. `uv run --locked pyrefly check` fails on new diagnostics;
existing ones remain visible in the editor. After fixing existing diagnostics,
run `uv run --locked pyrefly check --prune-baseline` and commit the reduced
baseline. Do not regenerate it to hide new errors.

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
