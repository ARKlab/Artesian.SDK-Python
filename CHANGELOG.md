# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Data Quality DTOs (rule configurations, alert triggers, schedule definitions, outlier models) decode to their concrete types and reject unknown discriminator values with `ValueError`.

### Changed

- JSON serialization now uses `msgspec` instead of `jsons`, which is no longer a dependency.
- Datetimes are sent as RFC 3339: naive values stay naive, UTC values end with `Z`, and the fractional part is omitted when it is zero (previously it was always sent with six digits).
- Mappings are sent as JSON objects unless the DTO field is explicitly marked to use the `Key`/`Value` array format; both shapes are still accepted when decoding.
- `NaN` and `Infinity` float values are rejected with `ValueError` when serializing.
