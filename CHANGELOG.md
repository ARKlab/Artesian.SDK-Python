# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Data Quality DTOs (rule configurations, alert triggers, schedule definitions, outlier models) decode to their concrete types and reject unknown discriminator values with `ValueError`.
- Support MAS and BidAsk completeness, freshness, and outlier rule configurations, plus compact check-result extraction.
- Add paged alert schedule events and optional ACL-aware Market Data details on Data Quality reads.
- Support optional Market Data details (`includeMarketData`) in TS and VTS Data Quality check-result extraction.

### Changed

- **BREAKING**: Data Quality reads default `includeMarketData` to `False`: Market Data names and providers are omitted unless requested.
- **BREAKING**: Data Quality endpoints require ACL grants on `/dataquality/dqrule/all` and `/dataquality/alertrule/all`; grants on `/featureflag/dqbeta` no longer apply.
- **BREAKING**: `includeDataQuality` on `readMarketDataRegistryById`, `readMarketDataRegistryByName` and `searchFacet` requires read access on `/dataquality/dqrule/all`.
- **BREAKING**: Limit ACL-aware Data Quality page sizes, result limits, and the assignment ID filters of the TS, VTS, MAS and BidAsk check-result extracts to 100; the `limit` of `getMarketDataDqStatusSummary` and `getDqRuleDqStatusSummary` was previously up to 1000.
- **BREAKING**: `AlertScheduleEventsDtoOutput.events` is now a `PagedResultDqCheckChangeEventDtoOutput` instead of `list[DqCheckChangeEventDtoOutput]`; replace `len(x.events)` and iteration over `x.events` with `x.events.data`.
- JSON serialization now uses `msgspec` instead of `jsons`, which is no longer a dependency.
- Datetimes are sent as RFC 3339: naive values stay naive, UTC values end with `Z`, and the fractional part is omitted when it is zero (previously it was always sent with six digits).
- Mappings are sent as JSON objects unless the DTO field is explicitly marked to use the `Key`/`Value` array format; both shapes are still accepted when decoding.
- `NaN` and `Infinity` float values are rejected with `ValueError` when serializing.

### Fixed

- `readAlertScheduleEvents` sends `scheduleTime` as a UTC instant ending with `Z`, as the service route requires.
