# Model Card: Mood Machine

This model card covers **both** versions of the Mood Machine classifier:
1. A **rule-based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit-learn

---

## 1. Model Overview

**Model type:** Both models were built and compared.

**Intended purpose:** Classify short social-media-style text messages into one of four mood labels: `positive`, `negative`, `neutral`, or `mixed`.

**How it works (brief):**

The rule-based version reads each post token by token and accumulates a numeric score. Positive-sentiment words (including slang like "bussin" and "fire") increase the score; negative words (like "terrible" or "exhausted") decrease it. The model also handles negation — phrases like "not happy" flip the polarity of the next word — and reads emoji characters directly from the text using a lookup table (🎉 = +2, 😭 = −2, etc.). The final score is mapped to a label using calibrated thresholds, with a special "mixed" path that fires when both positive and negative signals are present regardless of the net score.

The ML version uses a bag-of-words representation (CountVectorizer) fed into Logistic Regression trained on the labeled `SAMPLE_POSTS`. It learns statistical word-label associations purely from the data with no hand-written rules.

---

## 2. Data

**Dataset description:** The dataset contains 16 posts in `SAMPLE_POSTS`. The original starter provided 6 examples. We added 10 new posts to reach 16.

**Labeling process:** Labels were chosen by reading each post and asking what a neutral observer would most likely feel. Posts that clearly expressed only one emotion were easy to label. Posts with "but" or "however" (e.g., "So exhausted but honestly so proud") were labeled "mixed." Ambiguous cases like "This is fine" and "It's fine I'm fine everything is fine 🙂" were labeled "neutral" since the surface emotion is flat — even though the 🙂 is often sarcastic in context.

**Important characteristics of the dataset:**

The dataset intentionally includes diverse language styles to stress-test both classifiers. It contains standard English, slang ("no cap", "bussin", "trash", "mid"), emojis (🎉, 😭, 🙂, 😩), sarcasm ("I absolutely love getting stuck in traffic for two hours", "Oh great another Monday"), and mixed-emotion posts ("Lowkey stressed about finals but I got this").

**Possible issues with the dataset:** The dataset is very small (16 examples), which limits the ML model's generalization. Sarcasm posts were labeled by the intended meaning (negative), not the literal words, which creates a systematic mismatch for any keyword-based system. "Neutral" and "mixed" are underrepresented compared to "positive" and "negative."

---

## 3. How the Rule-Based Model Works

**Scoring rules:**

The `preprocess` method lowercases text, strips punctuation while preserving apostrophes (so "don't" stays intact), and extracts emoji characters before they are removed by the punctuation filter. Each emoji is added as its own token.

The `score_text` method loops over tokens and applies four types of scoring:
- Standard positive words give +1; negative words give −1.
- "Heavy" words (love, hate, amazing, terrible, exhausted, proud, etc.) are weighted ×2, giving ±2.
- Negation words (not, never, don't, can't, etc.) look ahead one token and flip its polarity. "Not happy" contributes −1 instead of +1; "not bad" contributes +1 instead of −1.
- Emoji tokens contribute directly from a lookup table (🎉 = +2, 😭 = −2, 😩 = −2, etc.).
- Slang tokens (bussin, fire, trash, mid) contribute from a separate slang table.

The `predict_label` method uses a threshold of ±2: scores ≥ 2 are "positive," scores ≤ −2 are "negative." Scores between −1 and +1 are "neutral" unless both positive and negative signals were detected, in which case the label is "mixed."

**Strengths of this approach:** The model is fully transparent — every prediction can be explained by citing the exact words and emoji that fired. Negation handling works reliably for simple "not X" patterns. Slang and emoji support extends coverage beyond standard English vocabulary. Accuracy on the labeled dataset is **88% (14/16)**.

**Weaknesses of this approach:** The model cannot detect sarcasm. "I absolutely love getting stuck in traffic" scores +2 because the word "love" fires without any negative context the model can see. Similarly, "Oh great another Monday" scores +1 because "great" is literally positive. Any word not in the vocabulary lists is invisible to the model.

---

## 4. How the ML Model Works

**Features used:** Bag-of-words representation via `CountVectorizer`. Each post becomes a sparse vector of word counts over the vocabulary seen during training.

**Training data:** Trained on all 16 examples in `SAMPLE_POSTS` / `TRUE_LABELS`. Because we evaluate on the same data used for training, reported accuracy is training accuracy — not generalization accuracy on unseen posts.

**Training behavior:** With only 16 examples, the ML model typically achieves 100% training accuracy because it overfits perfectly to the small dataset. Adding or changing even one label noticeably shifts predictions on other posts, showing extreme sensitivity to data choices.

**Strengths and weaknesses:** The ML model automatically learns which words correlate with which labels without manual rules. However, on a dataset this small it memorizes rather than generalizes. It is also more sensitive to label noise — contradictory signals from sarcasm posts are hard for it to resolve.

---

## 5. Evaluation

**How the model was evaluated:** Both versions were evaluated by running predictions on the full 16-post `SAMPLE_POSTS` dataset and comparing predictions to `TRUE_LABELS`.

**Rule-based results:** 14/16 correct → **88% accuracy**.

**Examples of correct predictions:**
- `"I passed my driving test 🎉🎉"` → positive (score +4 from two 🎉 emojis, each worth +2).
- `"I hate how much I love this show"` → mixed (both "hate" and "love" fire, net score 0).
- `"I am not happy about this"` → negative (negation flips "happy" from +1 to −1, score −1 with no competing positive).

**Examples of incorrect predictions:**
- `"I absolutely love getting stuck in traffic for two hours"` → predicted positive, true negative. The word "love" fires as +2 but the sarcasm is invisible. There are no negative words in the sentence.
- `"Oh great another Monday"` → predicted positive, true negative. "Great" scores +1; the model has no mechanism to recognize this is culturally a complaint.

---

## 6. Limitations

The two most important limitations are sarcasm blindness and vocabulary brittleness. Any sentence where the literal words suggest one emotion but the intended meaning is the opposite will fool the rule-based model. "I love traffic" and "I love puppies" are indistinguishable to it. Additionally, any word not explicitly in the vocabulary lists is silently ignored.

The dataset is also too small for the ML model to generalize. Because it trains and evaluates on the same 16 posts, its 100% training accuracy is misleading; it would likely perform much worse on posts it has never seen.

Finally, the model was built primarily on standard American internet English. It may misinterpret slang from other dialects, non-English loanwords, or culturally specific references.

---

## 7. Ethical Considerations

Automated mood detection applied to real people's messages carries meaningful risks. A system that misclassifies distress as neutral or positive could suppress a flag that a person needs support. The sarcasm failure case is especially concerning: "I'm totally fine, everything is great" from someone who is not fine could score as highly positive.

The model is also optimized for the specific slang and emoji patterns reflected in the 16 training posts, which reflect a particular cultural and linguistic context. Posts in AAVE, non-English languages written in the Latin alphabet, or regional slang not in the word lists will receive degraded accuracy — a form of representation bias.

Privacy is another concern. Mood classifiers are often deployed on private messages people share without expecting analysis. Any real deployment should be transparent about when and how mood inference is applied.

---

## 8. Ideas for Improvement

The most impactful short-term improvements would be adding more labeled examples (at least 100–200) and introducing a real held-out test set so accuracy reflects generalization, not memorization. For the rule-based model, a sarcasm detector — even a simple one that checks for phrases like "I love [negative_noun]" — would address the biggest failure category. Replacing `CountVectorizer` with TF-IDF would reduce the ML model's bias toward frequent but low-information words. Longer term, a small pre-trained transformer (such as DistilBERT fine-tuned on sentiment data) would handle sarcasm, context, and mixed emotions far more reliably than either approach used here.
