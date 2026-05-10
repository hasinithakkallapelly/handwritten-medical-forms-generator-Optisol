from __future__ import annotations

import re
from difflib import SequenceMatcher

import pandas as pd


REQUIRED_COLUMNS = {"filename", "ocr_text"}


def normalize_text(value: object) -> str:
    text = "" if value is None else str(value)
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def similarity_score(expected: object, observed: object) -> float:
    expected_text = normalize_text(expected)
    observed_text = normalize_text(observed)
    if not expected_text and not observed_text:
        return 100.0
    if not expected_text or not observed_text:
        return 0.0
    return round(SequenceMatcher(None, expected_text, observed_text).ratio() * 100, 2)


def evaluate_ocr_results(ground_truth: pd.DataFrame, ocr_results: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS - set(ocr_results.columns)
    if missing:
        raise ValueError(f"OCR results CSV is missing required column(s): {', '.join(sorted(missing))}")

    if "filename" not in ground_truth.columns or "ground_truth_text" not in ground_truth.columns:
        raise ValueError("Ground truth data must include filename and ground_truth_text columns.")

    merged = ground_truth[["filename", "ground_truth_text"]].merge(
        ocr_results[["filename", "ocr_text"]],
        on="filename",
        how="left",
    )
    merged["ocr_text"] = merged["ocr_text"].fillna("")
    merged["similarity"] = merged.apply(
        lambda row: similarity_score(row["ground_truth_text"], row["ocr_text"]),
        axis=1,
    )
    merged["status"] = pd.cut(
        merged["similarity"],
        bins=[-1, 50, 80, 100],
        labels=["Needs review", "Usable", "Strong"],
    )
    return merged
