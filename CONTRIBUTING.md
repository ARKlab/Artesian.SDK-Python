# How to Contribute

## 1. Create venv

Create a virtual env with a given python version. Use the lowest supported one (3.8 currently).
Upgrade pip (requires >=21.4) to be able to do editable install.
Then install all dependencies, including dev ones.

```sh
py -3.8 -m venv .venv
pip install --upgrade pip
pip install -e '.[dev]'
```

## 2. Run tests

Easy.

```sh
pytest
```
