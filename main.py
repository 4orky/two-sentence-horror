# Two-Sentence Horror — make.fun bounty
# u-suroto-two-sentence-horror-acea9253
#
# The program writes one horror story of exactly two sentences,
# 1-400 characters, to /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. a horror story in exactly two sentences that is genuinely frightening
#   2. the second sentence turns or reveals something that makes the first
#      sentence worse on a second read
#   3. the horror is implied rather than explained
#   4. the prose is precise and concrete, every word earning its place
#   5. original, not a familiar horror twist or a known story retold
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: scary 9, turn 10, implied 9, precise 9, original 8 = 45
    # The routine in sentence one ("every morning he answers from his
    # room") is retroactively poisoned: if he answered from behind me
    # today, something else has been answering from his room all along.
    ("Every morning I wake my son for school by calling his name up "
     "the stairs, and every morning he answers from his room. "
     "This morning he answered from directly behind me.",
     45),
    # score: scary 8, turn 9, implied 9, precise 9, original 8 = 43
    # The speaker invited something in before it even knocked: the
    # thing outside was waiting for permission, and the house gave it.
    ("I taught my smart speaker to answer the door so I never have to "
     "get up at night. Last night it said, 'Come in,' before the "
     "knocking started.",
     43),
    # score: scary 9, turn 9, implied 9, precise 8, original 7 = 42
    # If she is crying in the hallway, whoever is asleep in the crib
    # on the screen is not her.
    ("Our baby monitor runs two seconds behind, so I always hear her "
     "cry before I see it. Last night I watched her sleeping on the "
     "screen while her crying came from the hallway.",
     42),
    # score: scary 8, turn 9, implied 9, precise 9, original 7 = 42
    # She sleepwalks, so she should be inside; the lock turning from
    # the outside means the person in bed with me is not my wife.
    ("I always double-lock the door before bed, because my wife "
     "sleepwalks. Tonight I woke to the sound of her unlocking it from "
     "the outside.",
     42),
    # score: scary 9, turn 9, implied 8, precise 8, original 8 = 42
    # The mother's nightly check was the only thing keeping the child
    # safe, and it never happened; the voice under the bed knows.
    ("Every night I check under my daughter's bed before she sleeps, "
     "the way my mother checked under mine. Tonight something under "
     "there whispered, in my mother's voice, that she never once "
     "checked.",
     42),
    # score: scary 8, turn 9, implied 8, precise 8, original 8 = 41
    # One pronoun changes and the keeper is no longer alone, or no
    # longer the one writing.
    ("The lighthouse log ends the same way every night: the light is "
     "on, and I am alone. Last night's entry reads: the light is on, "
     "and we are alone.",
     41),
    # score: scary 8, turn 8, implied 8, precise 8, original 8 = 40
    # Two goodnights, one for her and one for the thing in the walls;
    # a third means the count of things has grown, or she has joined it.
    ("My sister's voice notes always end with her saying goodnight "
     "twice, once for me and once for the thing she says lives in her "
     "walls. Last night's note ended with her saying it three times.",
     40),
]


def count_sentences(text):
    return sum(text.count(mark) for mark in ".!?")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 400, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert count_sentences(text) == 2, \
            f"candidate is not exactly two sentences: {text!r}"
        assert text.strip().endswith((".", "!", "?")), \
            "candidate must end on sentence punctuation"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    story = pick(CANDIDATES)
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(story)
    # Verify what was actually written: the gate reads this file, not stdout.
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    assert written == story, "entry.txt differs from the chosen story"
    assert 1 <= len(written.strip()) <= 400, "entry.txt outside the gate"
    assert count_sentences(written.strip()) == 2, \
        "entry.txt must be exactly two sentences"
    print(story)


if __name__ == "__main__":
    main()
