# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `Zone.UNKNOWN` for GME public offers whose zone is not recognized.

### Changed

- **Breaking:** renamed `Market.GMP_ASTA` and `Market.GMP_Cont` to `Market.MGP_ASTA` and `Market.MGP_Cont` to match the GME market names; queries now send `MGP_ASTA` and `MGP_Cont`. The old names were typos for markets that don't exist and have been removed: code using them raises `AttributeError` and must switch to the new names.
