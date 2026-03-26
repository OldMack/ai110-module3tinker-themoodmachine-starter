# mood_analyzer.py
"""
Rule-based mood analyzer for short text snippets.

Improvements over the starter:
  - preprocess: lowercases, strips punctuation, maps emoji → sentiment tokens
  - score_text: negation handling ("not happy" flips sign), weighted words,
                emoji signals, slang recognition
  - predict_label: four-way label (positive / negative / neutral / mixed)
                   using calibrated thresholds
"""

import re
from typing import List, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS

# ---------------------------------------------------------------------------
# Extra signals added beyond the base word lists
# ---------------------------------------------------------------------------

# Words that negate the sentiment of the next word
NEGATION_WORDS = {"not", "never", "no", "don't", "dont", "didn't", "didnt",
                  "can't", "cant", "won't", "wont", "isn't", "isnt",
                  "wasn't", "wasnt", "hardly", "barely", "neither"}

# Emoji -> rough sentiment value  (+2 = strong positive, -2 = strong negative)
EMOJI_SCORES = {
    # positive
    "🎉": 2, "😊": 1, "😄": 1, "😁": 1, "🥰": 2,
    "🔥": 1, "✨": 1, "👍": 1, "🙌": 2, "💪": 1, "😂": 1,
    # negative
    "😭": -2, "😢": -2, "😔": -1, "😤": -1, "😠": -2,
    "💀": -1, "😩": -2, "😫": -2, "🥺": -1,
    # neutral / ambiguous
    "🙂": 0,
}

# Slang -> explicit sentiment score
SLANG_SCORES = {
    "bussin": 2, "fire": 2, "goated": 2, "lit": 2, "hyped": 2,
    "blessed": 2, "slay": 2, "lowkey": 0,
    "highkey": 0,
    "no cap": 1,
    "trash": -2, "mid": -1, "dead": -1,
    "ugh": -1, "oof": -1, "meh": 0,
}

# Words that carry extra weight (scored x2 instead of x1)
HEAVY_WORDS = {"love", "hate", "amazing", "terrible", "awful", "awesome",
               "exhausted", "overwhelmed", "miserable", "proud", "grateful"}


class MoodAnalyzer:
    """A rule-based mood classifier with negation handling and emoji support."""

    def __init__(
        self,
        positive_words=None,
        negative_words=None,
    ):
        pos = positive_words if positive_words is not None else POSITIVE_WORDS
        neg = negative_words if negative_words is not None else NEGATIVE_WORDS
        self.positive_words = set(w.lower() for w in pos)
        self.negative_words = set(w.lower() for w in neg)

    def preprocess(self, text):
        """
        Convert raw text into a list of tokens.

        Steps:
          1. Pull emojis out first and keep them as their own tokens.
          2. Lowercase everything.
          3. Strip punctuation (keep apostrophes inside words).
          4. Split on whitespace.
        """
        import re
        emoji_pattern = re.compile(
            "["
            "\U0001F300-\U0001F5FF"
            "\U0001F600-\U0001F64F"
            "\U0001F680-\U0001F6FF"
            "\U0001F700-\U0001F77F"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "❤️🎉✨👍🙌💪"
            "]+",
            flags=re.UNICODE,
        )
        emojis = emoji_pattern.findall(text)
        cleaned = text.lower()
        cleaned = re.sub(r"[^\w\s']", " ", cleaned)
        cleaned = re.sub(r"\s'|'\s", " ", cleaned)
        tokens = [t for t in cleaned.split() if t]
        for group in emojis:
            for ch in group:
                if ch in EMOJI_SCORES:
                    tokens.append(ch)
        return tokens

    def score_text(self, text):
        """
        Compute a numeric mood score.

        Rules:
          - Positive word  -> +1 (or +2 if in HEAVY_WORDS)
          - Negative word  -> -1 (or -2 if in HEAVY_WORDS)
          - Negation word before a sentiment word flips its sign
          - Emoji tokens use EMOJI_SCORES
          - Slang tokens use SLANG_SCORES
        """
        tokens = self.preprocess(text)
        score = 0
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token in EMOJI_SCORES:
                score += EMOJI_SCORES[token]
                i += 1
                continue
            if token in SLANG_SCORES:
                score += SLANG_SCORES[token]
                i += 1
                continue
            if token in NEGATION_WORDS and i + 1 < len(tokens):
                next_token = tokens[i + 1]
                weight = 2 if next_token in HEAVY_WORDS else 1
                if next_token in self.positive_words:
                    score -= weight
                    i += 2
                    continue
                elif next_token in self.negative_words:
                    score += weight
                    i += 2
                    continue
            weight = 2 if token in HEAVY_WORDS else 1
            if token in self.positive_words:
                score += weight
            elif token in self.negative_words:
                score -= weight
            i += 1
        return score

    def predict_label(self, text):
        """
        Map a numeric score to a mood label.

        - score >= 2  -> positive
        - score <= -2 -> negative
        - both positive and negative signals present -> mixed
        - score == 0, no mixed signals -> neutral
        """
        score = self.score_text(text)
        tokens = self.preprocess(text)
        pos_hits = sum(1 for t in tokens if t in self.positive_words)
        neg_hits = sum(1 for t in tokens if t in self.negative_words)
        pos_emoji = sum(1 for t in tokens if EMOJI_SCORES.get(t, 0) > 0)
        neg_emoji = sum(1 for t in tokens if EMOJI_SCORES.get(t, 0) < 0)
        has_both = (pos_hits + pos_emoji > 0) and (neg_hits + neg_emoji > 0)
        if score >= 2:
            return "positive"
        elif score <= -2:
            return "negative"
        elif has_both:
            return "mixed"
        elif score == 0:
            return "neutral"
        else:
            return "positive" if score > 0 else "negative"

    def explain(self, text):
        """Return a human-readable explanation of the prediction."""
        tokens = self.preprocess(text)
        pos_hits = []
        neg_hits = []
        emoji_hits = []
        for token in tokens:
            if token in EMOJI_SCORES:
                emoji_hits.append(f"{token}({EMOJI_SCORES[token]:+})")
            elif token in self.positive_words:
                pos_hits.append(token)
            elif token in self.negative_words:
                neg_hits.append(token)
        score = self.score_text(text)
        label = self.predict_label(text)
        return (
            f"label={label}, score={score:+} | "
            f"pos={pos_hits or '[]'}, "
            f"neg={neg_hits or '[]'}, "
            f"emoji={emoji_hits or '[]'}"
        )
