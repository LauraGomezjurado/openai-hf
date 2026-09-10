"""Loaders for the recovered Part 1 tables, shared by every figure."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PROC = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw" / "metr"
CPU = ROOT / "results" / "cpu"
OUT = ROOT / "results" / "figures"

TIME_COLS = [
    "start_utc",
    "end_utc",
    "read_utc",
    "write_utc",
    "hfStart_utc",
    "hfEnd_utc",
]

WINDOW_START = pd.Timestamp("2026-07-06T00:00:00Z")
WINDOW_END = pd.Timestamp("2026-07-14T00:00:00Z")


def agents() -> pd.DataFrame:
    """The 1,206 recovered agent timelines."""
    df = pd.read_csv(PROC / "metr_agents.csv")
    for col in TIME_COLS:
        df[col] = pd.to_datetime(df[col], utc=True, format="ISO8601")
    df["handle"] = df["snapshot_row_id"].map(handles())
    return df


def workstreams() -> pd.DataFrame:
    """1,772 sparse hourly rows, unpivoted to 12,404 workstream x purpose cells."""
    df = pd.read_csv(PROC / "metr_workstream_counts.csv")
    df["hour_utc"] = pd.to_datetime(df["hour_utc"], utc=True, format="ISO8601")
    return df


def _raw_js(name: str, var: str) -> dict:
    text = (RAW / name).read_text(encoding="utf-8")
    start = text.index("{", text.index(var))
    obj, _ = json.JSONDecoder().raw_decode(text[start:])
    return obj


def timeline_asset() -> dict:
    """The parsed `AGENT_TIMELINE_DATA` object, including its 12 annotations."""
    return _raw_js("agent-data.js", "AGENT_TIMELINE_DATA")


def handles() -> dict[int, str]:
    """The 74 message-scan handles the asset ships as row labels."""
    raw = _raw_js("agent-data.js", "AGENT_TIMELINE_HANDLES")
    return {int(k): v for k, v in raw.items()}


def annotations() -> pd.DataFrame:
    """The 12 anchored annotations, typed by provenance."""
    ann = timeline_asset()["annotations"]
    rows = []
    for i, a in enumerate(ann):
        text = a.get("quote") or a.get("paraphrase") or a["title"]
        rows.append(
            {
                "idx": i,
                "row_id": a["agent"],
                "time": WINDOW_START + pd.Timedelta(seconds=a["time"]),
                "kind": a["kind"],
                "title": a["title"],
                "detail": a.get("detail"),
                "text": text,
                # METR's own typography: braces mark paraphrased reasoning.
                "provenance": (
                    "quote"
                    if "quote" in a
                    else ("paraphrase" if "paraphrase" in a else "event")
                ),
                "approximate": bool(a.get("approximateTime")),
            }
        )
    return pd.DataFrame(rows)


def featured_rows() -> list[int]:
    """The 19 rows the report singled out in its own figure."""
    return list(timeline_asset()["featuredAgents"])


def declared_participants() -> int:
    return int(timeline_asset()["verifiedHfParticipants"])


def timing_sensitivity() -> pd.DataFrame:
    return pd.read_csv(CPU / "timing_sensitivity.csv")


def ordering_issues() -> pd.DataFrame:
    return pd.read_csv(CPU / "timeline_ordering_issues.csv")


def missingness() -> pd.DataFrame:
    return pd.read_csv(CPU / "missingness_by_group.csv")


def read_anchored_scores() -> pd.DataFrame:
    return pd.read_csv(CPU / "read_anchored_scores.csv")


def workstream_forecast_scores() -> pd.DataFrame:
    return pd.read_csv(CPU / "workstream_forecast_scores.csv")


def workstream_predictions() -> pd.DataFrame:
    df = pd.read_csv(CPU / "workstream_predictions.csv")
    for col in df.columns:
        if col.endswith("_utc") or col in ("bin_start", "hour_utc"):
            df[col] = pd.to_datetime(df[col], utc=True, format="ISO8601")
    return df


def read_anchored_predictions() -> pd.DataFrame:
    return pd.read_csv(CPU / "read_anchored_predictions.csv")


def ensure_out() -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    return OUT
