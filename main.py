#!/usr/bin/env python3
"""two-sentence-horror — a single two-sentence horror story.

The brief asks for one story, exactly two sentences, between 1 and
400 characters, that is genuinely frightening. The second sentence has
to reframe the first: after reading it, the first sentence means
something worse than it did on its own. The dread should stay
implied — nothing is named, nothing is explained — and the prose
should be plain and concrete, with no wasted words. The twist must be
the author's own, not a retread of a familiar horror beat.

Ten drafts were written against that brief and marked on five
measures, each out of ten: dread, reversal, implication, economy and
freshness. The marks below are the author's own judgement, made while
drafting. The draft with the highest weighted total is the entry;
when two drafts tie, the shorter one wins, because a horror story
this short has no room for a spare syllable.

Running the program writes the winning story to /output/entry.txt
and prints it. The result is the same on every run.
"""

import hashlib
import re
import sys
from pathlib import Path

# How much each measure counts when the drafts are ranked. Dread and
# the reversal carry the story, so they weigh double; the other three
# keep the prose honest.
WEIGHTS = {"dread": 2, "reversal": 2, "implication": 1, "economy": 1, "freshness": 1}

# Each draft is a mapping with the text and one mark per measure.
# The notes beside a draft say, in one line, where its scare lives.
DRAFTS = [
    {
        "text": (
            "Every morning I wake my son for school by calling his name "
            "up the stairs, and every morning he answers from his room. "
            "This morning he answered from directly behind me."
        ),
        "marks": {"dread": 9, "reversal": 10, "implication": 9, "economy": 9, "freshness": 8},
        # The morning routine was the alibi: a voice answering from the
        # bedroom every day means something else has lived in that room.
    },
    {
        "text": (
            "My daughter asked me to leave the hall light on, because "
            "the man in her closet only comes out in the dark. I turned "
            "the light off to prove him imaginary, and he thanked me."
        ),
        "marks": {"dread": 9, "reversal": 9, "implication": 8, "economy": 9, "freshness": 8},
        # The parent's reassurance is the invitation; the thank-you
        # confirms the man was waiting for permission, not for darkness.
    },
    {
        "text": (
            "The voicemail from my late husband plays every year on our "
            "anniversary, exactly as I saved it. This year it ends with "
            "him asking who the man sleeping beside me is."
        ),
        "marks": {"dread": 9, "reversal": 9, "implication": 9, "economy": 8, "freshness": 8},
        # A recording cannot learn new facts, so either it was never a
        # recording, or the dead have been listening all along.
    },
    {
        "text": (
            "I finally taught my parrot to say goodnight, and now it says "
            "it every evening at nine. Last night it said it at three in "
            "the morning, in my dead mother's voice."
        ),
        "marks": {"dread": 8, "reversal": 9, "implication": 9, "economy": 8, "freshness": 8},
        # The bird only repeats what it hears; the voice it borrowed
        # means someone spoke those words in this house at 3 a.m.
    },
    {
        "text": (
            "Our new house came with a nursery the estate agent swore had "
            "never been used. Every night since we moved in, the mobile "
            "above the empty crib turns by itself."
        ),
        "marks": {"dread": 8, "reversal": 8, "implication": 9, "economy": 8, "freshness": 7},
        # An unused room should be still; a mobile that turns needs a
        # hand, or a breeze from a door that was never opened.
    },
    {
        "text": (
            "I set my alarm for six every morning so I can hear my wife "
            "make coffee downstairs. This morning the kettle boiled at "
            "six, and my wife has been away for a week."
        ),
        "marks": {"dread": 8, "reversal": 9, "implication": 8, "economy": 9, "freshness": 7},
        # The kettle knows the routine better than the household does;
        # somebody has been keeping the morning going in her absence.
    },
    {
        "text": (
            "The lift in my building has always stopped at my floor "
            "without me pressing anything. Yesterday it stopped at the "
            "floor that was sealed off after the fire in 1987."
        ),
        "marks": {"dread": 8, "reversal": 8, "implication": 8, "economy": 8, "freshness": 8},
        # A lift that knows your floor is convenient; a lift that knows
        # a floor nobody can reach is carrying a passenger you cannot see.
    },
    {
        "text": (
            "I write my shopping lists on the fridge in the same blue pen "
            "every week. This morning's list is in my handwriting, and it "
            "is written in a pen I threw away years ago."
        ),
        "marks": {"dread": 7, "reversal": 8, "implication": 9, "economy": 8, "freshness": 8},
        # The list is in the author's hand, yet the author never wrote
        # it; something has been practising being them.
    },
    {
        "text": (
            "My grandfather's clock chimes thirteen times at midnight, "
            "and my family laughs it off as a broken gear. Last night it "
            "chimed twelve times, and the house went quiet."
        ),
        "marks": {"dread": 7, "reversal": 8, "implication": 8, "economy": 8, "freshness": 7},
        # The broken chime was the house's heartbeat; when it finally
        # keeps correct time, whatever kept it broken has left — or arrived.
    },
    {
        "text": (
            "The dog barks at the window every night at the same minute, "
            "though our street has been empty for years. Tonight the dog "
            "is asleep, and something outside is barking back."
        ),
        "marks": {"dread": 8, "reversal": 8, "implication": 8, "economy": 8, "freshness": 7},
        # The dog was the alarm; the night the alarm sleeps, the thing
        # it watched has learned to imitate the alarm itself.
    },
]

ENTRY_PATH = Path("/output/entry.txt")

# The brief's hard gates: two sentences, 1-400 characters.
MIN_CHARS = 1
MAX_CHARS = 400
SENTENCES_WANTED = 2

# A sentence ends on one of these marks. Abbreviations would fool a
# naive counter, so the splitter below only counts a mark that is
# followed by a space and a capital letter, or by the end of the text.
TERMINATORS = frozenset(".!?")
_SENTENCE_END = re.compile(r"[.!?](?=\s+[A-Z]|\s*$)")


def tally(marks):
    """Weighted total of one draft's marks."""
    return sum(marks[name] * WEIGHTS[name] for name in WEIGHTS)


def sentence_total(text):
    """How many sentences the text holds, by terminal punctuation."""
    return len(_SENTENCE_END.findall(text.strip()))


def passes_gates(text):
    """True when a draft satisfies every hard gate in the brief."""
    stripped = text.strip()
    if not MIN_CHARS <= len(stripped) <= MAX_CHARS:
        return False
    if sentence_total(stripped) != SENTENCES_WANTED:
        return False
    if stripped[-1] not in TERMINATORS:
        return False
    return True


def choose(drafts):
    """Return the winning draft: highest weighted total, then shortest."""
    ranked = []
    for draft in drafts:
        text = draft["text"]
        if not passes_gates(text):
            raise ValueError("draft fails the brief's gates: %r" % text)
        ranked.append((tally(draft["marks"]), -len(text), text))
    ranked.sort(reverse=True)
    return ranked[0][2]


def digest(text):
    """Short fingerprint of the winning text, for the run log."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def emit():
    """Pick the winner, write it to the entry file, and verify it."""
    winner = choose(DRAFTS)
    ENTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENTRY_PATH.write_text(winner, encoding="utf-8")
    reread = ENTRY_PATH.read_text(encoding="utf-8")
    if reread != winner:
        raise ValueError("entry file does not match the chosen story")
    if not passes_gates(reread):
        raise ValueError("entry file fails the brief's gates")
    # The run log goes to stderr so stdout carries only the story itself.
    print("sha256:%s chars:%d" % (digest(winner), len(winner)), file=sys.stderr, flush=True)
    print(winner)


if __name__ == "__main__":
    emit()
