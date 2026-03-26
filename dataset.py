"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS:   short example posts for evaluation and training
  - TRUE_LABELS:    human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------
POSITIVE_WORDS = [
    "happy", "great", "good", "love", "excited", "awesome", "fun",
    "chill", "relaxed", "amazing",
    # Added: common slang positives, emotion words, emoji-words
    "bussin", "fire", "goated", "lowkey", "blessed", "grateful",
    "proud", "hyped", "lit", "vibes", "hopeful", "thankful", "confident",
]

NEGATIVE_WORDS = [
    "sad", "bad", "terrible", "awful", "angry", "upset", "tired",
    "stressed", "hate", "boring",
    # Added: stronger negatives and stress words
    "miserable", "exhausted", "frustrated", "overwhelmed", "drained",
    "anxious", "disappointed", "rough", "trash", "dead",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------
# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    # ---- original 6 ----
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",

    # ---- added: slang ----
    "No cap this assignment is actually bussin",          # positive slang
    "Lowkey stressed about finals but I got this",        # mixed
    "That exam was straight trash no cap",                # negative slang

    # ---- added: emojis ----
    "I passed my driving test 🎉🎉",                      # positive
    "Missed the bus again 😭😭",                          # negative
    "It's fine I'm fine everything is fine 🙂",          # neutral/sarcastic

    # ---- added: sarcasm ----
    "I absolutely love getting stuck in traffic for two hours",  # negative (sarcasm)
    "Oh great another Monday",                            # negative (sarcasm)

    # ---- added: mixed / ambiguous ----
    "So exhausted but honestly so proud of how far I have come",  # mixed
    "I hate how much I love this show",                   # mixed
]

# Human labels for each post above.
# Allowed labels: "positive", "negative", "neutral", "mixed"
TRUE_LABELS = [
    # ---- original 6 ----
    "positive",   # "I love this class so much"
    "negative",   # "Today was a terrible day"
    "mixed",      # "Feeling tired but kind of hopeful"
    "neutral",    # "This is fine"
    "positive",   # "So excited for the weekend"
    "negative",   # "I am not happy about this"

    # ---- added ----
    "positive",   # "No cap this assignment is actually bussin"
    "mixed",      # "Lowkey stressed about finals but I got this"
    "negative",   # "That exam was straight trash no cap"
    "positive",   # "I passed my driving test"
    "negative",   # "Missed the bus again"
    "neutral",    # "It's fine I'm fine everything is fine"
    "negative",   # "I absolutely love getting stuck in traffic..." (sarcasm)
    "negative",   # "Oh great another Monday" (sarcasm)
    "mixed",      # "So exhausted but honestly so proud..."
    "mixed",      # "I hate how much I love this show"
]

assert len(SAMPLE_POSTS) == len(TRUE_LABELS), (
    f"Length mismatch! SAMPLE_POSTS={len(SAMPLE_POSTS)}, "
    f"TRUE_LABELS={len(TRUE_LABELS)}"
)
