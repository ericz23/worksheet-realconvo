from __future__ import annotations

import csv
import sys
import statistics
from pathlib import Path
from typing import List, Tuple, Optional

import matplotlib.pyplot as plt


def load_scores(csv_path: Path) -> Tuple[List[float], List[float], Optional[List[float]]]:
    """Load intent, semantic, and optional policy adherence scores from the evaluation CSV."""
    intents: List[float] = []
    semantics: List[float] = []
    policies: List[float] = []
    has_policy = False

    with csv_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        
        # Check if 'policy_adherence' exists in the header
        if reader.fieldnames and "policy_adherence" in reader.fieldnames:
            has_policy = True
            
        for idx, row in enumerate(reader, start=2):
            intent_raw = row.get("intent_match")
            semantic_raw = row.get("semantic_similarity")
            
            if intent_raw in (None, "") or semantic_raw in (None, ""):
                continue
            
            try:
                intents.append(float(intent_raw))
                semantics.append(float(semantic_raw))
                
                if has_policy:
                    policy_raw = row.get("policy_adherence")
                    if policy_raw not in (None, ""):
                        policies.append(float(policy_raw))
                        
            except ValueError as exc:
                raise ValueError(
                    f"Non-numeric score at CSV row {idx}"
                ) from exc
                
    return intents, semantics, (policies if has_policy and policies else None)


def plot_distributions(intent_scores: List[float], semantic_scores: List[float], policy_scores: Optional[List[float]] = None) -> None:
    """Plot histograms for score columns."""
    num_plots = 3 if policy_scores else 2
    fig, axes = plt.subplots(1, num_plots, figsize=(5 * num_plots, 4))
    
    # Handle single axis case if it were ever to happen, though here min is 2
    if num_plots == 1:
        axes = [axes]

    weights_intent = [1.0 / len(intent_scores)] * len(intent_scores)
    axes[0].hist(intent_scores, bins=20, color="#4c72b0", alpha=0.8, weights=weights_intent)
    axes[0].set_title("Intent Match Distribution")
    axes[0].set_xlabel("Intent Match")
    axes[0].set_ylabel("Proportion")

    weights_semantic = [1.0 / len(semantic_scores)] * len(semantic_scores)
    axes[1].hist(semantic_scores, bins=20, color="#55a868", alpha=0.8, weights=weights_semantic)
    axes[1].set_title("Semantic Similarity Distribution")
    axes[1].set_xlabel("Semantic Similarity")
    axes[1].set_ylabel("Proportion")
    
    if policy_scores:
        weights_policy = [1.0 / len(policy_scores)] * len(policy_scores)
        axes[2].hist(policy_scores, bins=20, color="#c44e52", alpha=0.8, weights=weights_policy)
        axes[2].set_title("Policy Adherence Distribution")
        axes[2].set_xlabel("Policy Adherence")
        axes[2].set_ylabel("Proportion")

    fig.suptitle("Evaluation Score Distributions")
    fig.tight_layout()
    plt.show()


def print_statistics(intent_scores: List[float], semantic_scores: List[float], policy_scores: Optional[List[float]] = None) -> None:
    """Print mean, median, and percentage > 0.5 for metrics."""
    if not intent_scores:
        print("No scores to analyze.")
        return

    print(f"\n--- Statistics (N={len(intent_scores)}) ---")

    # Intent Match
    i_mean = statistics.mean(intent_scores)
    i_median = statistics.median(intent_scores)
    i_gt_50 = sum(1 for x in intent_scores if x > 0.5)
    i_pct = (i_gt_50 / len(intent_scores)) * 100
    print(f"Intent Match:       Mean={i_mean:.2f}, Median={i_median:.2f}, >50%={i_pct:.1f}%")

    # Semantic Similarity
    s_mean = statistics.mean(semantic_scores)
    s_median = statistics.median(semantic_scores)
    s_gt_50 = sum(1 for x in semantic_scores if x > 0.5)
    s_pct = (s_gt_50 / len(semantic_scores)) * 100
    print(f"Semantic Similarity: Mean={s_mean:.2f}, Median={s_median:.2f}, >50%={s_pct:.1f}%")
    
    # Policy Adherence
    if policy_scores:
        p_mean = statistics.mean(policy_scores)
        p_median = statistics.median(policy_scores)
        p_gt_50 = sum(1 for x in policy_scores if x > 0.5)
        p_pct = (p_gt_50 / len(policy_scores)) * 100
        print(f"Policy Adherence:    Mean={p_mean:.2f}, Median={p_median:.2f}, >50%={p_pct:.1f}%")
        
    print("-" * 30 + "\n")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python plot_score_distributions.py <evaluation_csv>")
        sys.exit(1)

    csv_path = Path(sys.argv[1])
    if not csv_path.is_file():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    intent_scores, semantic_scores, policy_scores = load_scores(csv_path)
    print_statistics(intent_scores, semantic_scores, policy_scores)
    plot_distributions(intent_scores, semantic_scores, policy_scores)


if __name__ == "__main__":
    main()
