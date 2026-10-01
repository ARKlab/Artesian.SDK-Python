# Serde benchmark

`bench_serde.py` measures big Artesian payloads through the public adapter
(`artesianJsonSerialize`/`artesianJsonDeserialize`) and through `_Client.exec` with HTTP
mocked by `responses`, so it runs unchanged against any serializer backend.

```sh
uv run --locked python benchmark/bench_serde.py --rows 1000000 --out results.json
uv run --locked python benchmark/bench_serde.py --rows 100000 --memory   # adds a tracemalloc run
```

Cases (`--rows` = N):

- upserts with N rows: actual time series, market assessment (N x 2 products), bid/ask, auction;
  `serialize` builds builtins, `Client.exec POST` is the real wire path (encode + request);
- `TimeSerieData` with N Key/Value rows: typed deserialize from builtins and via `Client.exec GET`;
- query result with N records via `Client.exec GET` (untyped, `retcls=None`).

## Results

Linux, 4 vCPU, CPython 3.14. Times at N = 1,000,000 (single run), peak memory at N = 100,000
(`--memory`). Raw numbers are in `results/`.

| Case | jsons s | msgspec s | speed-up | jsons peak MiB | msgspec peak MiB |
|---|---:|---:|---:|---:|---:|
| upsert actual: serialize | 8.78 | 0.39 | 23× | 25 | 29 |
| upsert actual: Client.exec POST | 9.16 | 0.25 | 37× | 36 | 12 |
| upsert mas: serialize | 106.68 | 7.29 | 15× | 117 | 159 |
| upsert mas: Client.exec POST | 106.22 | 5.08 | 21× | 147 | 72 |
| upsert bidask: serialize | 51.31 | 4.03 | 13× | 78 | 101 |
| upsert bidask: Client.exec POST | 51.99 | 3.27 | 16× | 102 | 46 |
| upsert auction: serialize | 103.61 | 7.49 | 14× | 132 | 169 |
| upsert auction: Client.exec POST | 99.68 | 6.84 | 15× | 167 | 91 |
| TimeSerieData: deserialize | 12.71 | 0.30 | 43× | 11 | 17 |
| TimeSerieData: Client.exec GET | 13.97 | 0.40 | 35× | 42 | 24 |
| query result: Client.exec GET | 1.45 | 0.63 | 2× | 51 | 43 |

`serialize` returns builtins for tests and callers; with msgspec it first builds the wire structs,
hence higher peak memory than the `Client.exec` path, which encodes straight to bytes.
Dataclass-heavy upserts (MAS, bid/ask, auction) still spend most time converting dataclasses in Python.
