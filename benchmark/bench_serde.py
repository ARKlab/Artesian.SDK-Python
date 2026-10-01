"""Serde benchmark for large Artesian payloads.

Every case goes through the public adapter (`artesianJsonSerialize`/`artesianJsonDeserialize`) or
`_Client.exec` with HTTP mocked by `responses`, so the same script measures any serializer backend.
Response bodies are generated with the stdlib `json` module to keep inputs identical across backends.

    uv run --locked python benchmark/bench_serde.py --rows 1000000 [--memory] [--out results.json]
"""

import argparse
import asyncio
import json
import time
import tracemalloc
from collections.abc import Callable
from datetime import UTC, datetime, timedelta

import responses

from Artesian._ClientsExecutor.ArtesianJsonSerializer import artesianJsonDeserialize, artesianJsonSerialize
from Artesian._ClientsExecutor.Client import _Client
from Artesian.MarketData import (
    AuctionBids,
    AuctionBidValue,
    BidAskValue,
    MarketAssessmentValue,
    MarketDataIdentifier,
    UpsertData,
)
from Artesian.MarketData._Dto.TimeSerieData import TimeSerieData

BASE = "https://bench.local"
START = datetime(2020, 1, 1)  # noqa: DTZ001 - Artesian rows are naive local times


def _times(n: int) -> list[datetime]:
    return [START + timedelta(hours=i) for i in range(n)]


def _upsert(n: int, kind: str) -> UpsertData:
    upsert = UpsertData(MarketDataIdentifier("BENCH", kind), "CET", downloadedAt=datetime(2020, 1, 1, tzinfo=UTC))
    times = _times(n)
    if kind == "actual":
        upsert.rows = {t: float(i) for i, t in enumerate(times)}
    elif kind == "mas":
        # n report times x 2 products, i.e. 2n assessments.
        upsert.marketAssessment = {
            t: {"Feb-20": MarketAssessmentValue(open=1.0, close=2.0), "Mar-20": MarketAssessmentValue(settlement=3.0)}
            for t in times
        }
    elif kind == "bidask":
        upsert.bidAsk = {t: {"Feb-20": BidAskValue(bestBidPrice=1.0, lastQuantity=2.0)} for t in times}
    else:
        upsert.auctionRows = {
            t: AuctionBids(t, bid=[AuctionBidValue(1.0, 2.0)], offer=[AuctionBidValue(3.0, 4.0)]) for t in times
        }
    return upsert


def _timeserie_body(n: int) -> bytes:
    rows = [{"Key": t.isoformat(), "Value": float(i)} for i, t in enumerate(_times(n))]
    return json.dumps({"Type": "ActualTimeSerie", "Rows": rows}).encode()


def _query_body(n: int) -> bytes:
    rows = [
        {"P": "BENCH", "C": "Curve", "ID": 1, "T": t.isoformat() + "Z", "D": float(i)} for i, t in enumerate(_times(n))
    ]
    return json.dumps(rows).encode()


def _exec(
    method: str, body: bytes | None = None, obj: object = None, retcls: type | None = None
) -> Callable[[], object]:
    def run() -> object:
        with responses.RequestsMock() as rsps:
            if body is None:
                rsps.add(method, BASE + "/x", status=204)
            else:
                rsps.add(method, BASE + "/x", body=body, content_type="application/json")
            with _Client(BASE, "key") as c:
                return asyncio.run(c.exec(method, "/x", obj, retcls))

    return run


def _measure(fn: Callable[[], object], memory: bool) -> tuple[float, float | None]:
    start = time.perf_counter()
    fn()
    elapsed = time.perf_counter() - start
    if not memory:
        return elapsed, None
    tracemalloc.start()
    fn()
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    return elapsed, peak / 2**20


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=1_000_000)
    ap.add_argument("--memory", action="store_true", help="extra traced run per case for peak memory (slow)")
    ap.add_argument("--out", help="write results as JSON")
    args = ap.parse_args()
    n = args.rows

    ts_body, q_body = _timeserie_body(n), _query_body(n)
    ts_builtins = json.loads(ts_body)
    cases: list[tuple[str, int, Callable[[], object]]] = []
    for kind in ("actual", "mas", "bidask", "auction"):
        upsert = _upsert(n, kind)
        cases.append((f"upsert {kind}: serialize", 0, lambda u=upsert: artesianJsonSerialize(u)))
        cases.append((f"upsert {kind}: Client.exec POST", 0, _exec("POST", obj=upsert)))
    cases.append(("TimeSerieData: deserialize", 0, lambda: artesianJsonDeserialize(ts_builtins, TimeSerieData)))
    cases.append(("TimeSerieData: Client.exec GET", len(ts_body), _exec("GET", ts_body, retcls=TimeSerieData)))
    cases.append(("query result: Client.exec GET", len(q_body), _exec("GET", q_body)))

    results = []
    print(f"{'case':36} {'seconds':>9} {'peak MiB':>9} {'body MiB':>9}")
    for name, size, fn in cases:
        seconds, peak = _measure(fn, args.memory)
        results.append({"case": name, "rows": n, "seconds": seconds, "peak_mib": peak, "body_mib": size / 2**20})
        peak_s = f"{peak:9.1f}" if peak is not None else f"{'-':>9}"
        print(f"{name:36} {seconds:9.2f} {peak_s} {size / 2**20:9.1f}", flush=True)
    if args.out:
        with open(args.out, "w") as f:
            json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
