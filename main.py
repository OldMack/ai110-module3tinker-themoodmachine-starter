"""
Entry point for the Mood Machine rule-based mood analyzer.
"""

from typing import List
from mood_analyzer import MoodAnalyzer
from dataset import SAMPLE_POSTS, TRUE_LABELS


def evaluate_rule_based(posts: List[str], labels: List[str]) -> float:
    """
    Evaluate the rule-based MoodAnalyzer on a labeled dataset.
    Prints each text with its predicted label and the true label,
    then returns the overall accuracy as a float between 0 and 1.
    """
    analyzer = MoodAnalyzer()
    correct = 0
    total = len(posts)

    print("=== Rule-Based Evaluation on SAMPLE_POSTS ===")
    for text, true_label in zip(posts, labels):
        predicted_label = analyzer.predict_label(text)
        is_correct = predicted_label == true_label
        if is_correct:
            correct += 1
        marker = "OK" if is_correct else "XX"
        reason = analyzer.explain(text)
        print(f'  [{marker}] "{text}"')
        print(f'      predicted={predicted_label}, true={true_label}')
        print(f'      ({reason})')

    if total == 0:
        print("\nNo labeled examples to evaluate.")
        return 0.0

    accuracy = correct / total
    print(f"\nRule-based accuracy on SAMPLE_POSTS: {accuracy:.2f} ({correct}/{total})")
    return accuracy


def run_batch_demo() -> None:
    """
    Run the MoodAnalyzer on hand-crafted breaker sentences (Part 3).
    """
    analyzer = MoodAnalyzer()
    breakers = [
        "I love getting stuck in traffic",
        "sick beats bro",
        "I'm fine",
        "not bad at all",
        "I don't hate it",
        "this is so mid",
        "passed my exam but I'm exhausted",
    ]

    print("\n=== Batch Demo: Breaker Sentences ===")
    for text in breakers:
        reason = analyzer.explain(text)
        print(f'  "{text}"')
        print(f'      {reason}')


if __name__ == "__main__":
    evaluate_rule_based(SAMPLE_POSTS, TRUE_LABELS)
    run_batch_demo()
    print("\nTip: run `python ml_experiments.py` to try the ML model.")
