"""Utilities to parse word-level timestamps and segment conversations into turns.

This module provides:
- parse_words: parse the JSON string of word objects into typed Python records
- words_to_segments: build segments (candidate turns) using adaptive silence gaps
- build_llm_windows: format segments + metadata for LLM labeling prompts
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import json
import math
import re


@dataclass
class Word:
    text: str
    start: Optional[int]
    end: Optional[int]
    confidence: Optional[float]
    speaker: Optional[str]


@dataclass
class Segment:
    segment_id: int
    start_ms: int
    end_ms: int
    text: str
    duration_ms: int
    num_tokens: int
    avg_confidence: Optional[float]


def _safe_int(value: Any) -> Optional[int]:
    try:
        if value is None:
            return None
        return int(value)
    except Exception:
        return None


def _safe_float(value: Any) -> Optional[float]:
    try:
        if value is None:
            return None
        return float(value)
    except Exception:
        return None


def parse_words(words_json: str) -> List[Word]:
    """Parse the words JSON string into a list of Word.

    Args:
        words_json: JSON string of word dicts.

    Returns:
        List[Word] sorted by start time (unknown/missing timestamps placed last).
    """
    try:
        raw = json.loads(words_json or "[]")
    except Exception:
        raw = []

    words: List[Word] = []
    for item in raw if isinstance(raw, list) else []:
        words.append(
            Word(
                text=str(item.get("text", "")),
                start=_safe_int(item.get("start")),
                end=_safe_int(item.get("end")),
                confidence=_safe_float(item.get("confidence")),
                speaker=item.get("speaker"),
            )
        )

    words.sort(key=lambda w: (math.inf if w.start is None else w.start))
    return words


def _percentile(sorted_values: List[int], p: float) -> int:
    if not sorted_values:
        return 0
    if p <= 0:
        return sorted_values[0]
    if p >= 1:
        return sorted_values[-1]
    idx = int(round(p * (len(sorted_values) - 1)))
    return sorted_values[idx]


_PUNCT_BEFORE = re.compile(r"\s+([,\.!?;:])")


def _detokenize(tokens: List[str]) -> str:
    text = " ".join(t for t in tokens if t)
    text = _PUNCT_BEFORE.sub(r"\1", text)
    return text.strip()


def words_to_segments(
    words: List[Word],
    gap_ms: Optional[int] = None,
    adaptive: bool = True,
    min_gap_ms: int = 1500,
    max_gap_ms: int = 3000,
) -> List[Segment]:
    """Group words into segments by silence gaps.

    If gap_ms is not provided and adaptive=True, the gap threshold is the 95th
    percentile of observed inter-word gaps, clamped to [min_gap_ms, max_gap_ms].
    """
    # Collect valid gaps
    gaps: List[int] = []
    prev_end: Optional[int] = None
    for w in words:
        if prev_end is not None and w.start is not None and w.start >= 0 and prev_end >= 0:
            gaps.append(max(0, w.start - prev_end))
        if w.end is not None:
            prev_end = w.end

    if gap_ms is None and adaptive:
        gaps_sorted = sorted(gaps)
        p95 = _percentile(gaps_sorted, 0.95) if gaps_sorted else min_gap_ms
        gap_threshold = max(min_gap_ms, min(max_gap_ms, p95))
    else:
        gap_threshold = gap_ms if gap_ms is not None else min_gap_ms

    segments: List[Segment] = []
    cur_tokens: List[str] = []
    cur_start: Optional[int] = None
    prev_end = None
    conf_sum: float = 0.0
    conf_count: int = 0

    def flush_segment():
        nonlocal cur_tokens, cur_start, prev_end, conf_sum, conf_count
        if not cur_tokens or cur_start is None or prev_end is None:
            return
        seg_text = _detokenize(cur_tokens)
        duration = max(0, prev_end - cur_start)
        avg_conf = (conf_sum / conf_count) if conf_count > 0 else None
        segments.append(
            Segment(
                segment_id=len(segments),
                start_ms=cur_start,
                end_ms=prev_end,
                text=seg_text,
                duration_ms=duration,
                num_tokens=len(cur_tokens),
                avg_confidence=avg_conf,
            )
        )
        cur_tokens = []
        cur_start = None
        prev_end = None
        conf_sum = 0.0
        conf_count = 0

    for w in words:
        # Skip words missing timestamps entirely
        if w.start is None or w.end is None:
            continue
        if cur_start is None:
            cur_start = w.start
        # Boundary check
        if prev_end is not None and (w.start - prev_end) > gap_threshold:
            flush_segment()
            cur_start = w.start
        # Accumulate
        cur_tokens.append(w.text)
        if w.confidence is not None:
            conf_sum += w.confidence
            conf_count += 1
        prev_end = w.end

    flush_segment()
    return segments


def build_llm_windows(
    segments: List[Segment],
    metadata: Dict[str, Any],
    max_segments_per_window: int = 40,
    overlap: int = 2,
) -> List[Dict[str, Any]]:
    """Create LLM-ready windowed inputs from segments and metadata."""
    windows: List[Dict[str, Any]] = []
    i = 0
    n = len(segments)
    if max_segments_per_window <= 0:
        max_segments_per_window = 40
    if overlap < 0:
        overlap = 0

    base_payload = {
        "task": "speaker_labeling",
        "metadata": metadata,
        "instructions": [
            "Assign each segment a speaker: 'AGENT' or 'CUSTOMER'.",
            "Preserve order and time spans.",
            "If a segment is clearly a continuation by the same speaker, you may merge.",
            "Return only JSON matching the schema.",
        ],
    }

    while i < n:
        j = min(n, i + max_segments_per_window)
        window_segments = [
            {
                "segment_id": s.segment_id,
                "start_ms": s.start_ms,
                "end_ms": s.end_ms,
                "text": s.text,
            }
            for s in segments[i:j]
        ]
        payload = dict(base_payload)
        payload["segments"] = window_segments
        windows.append(payload)
        if j >= n:
            break
        i = j - overlap if overlap > 0 else j
    return windows


