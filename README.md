# two-sentence-horror

[![make.fun · u-suroto-two-sentence-horror-acea9253](https://make.fun/badge/u-suroto-two-sentence-horror-acea9253.svg)](https://make.fun/bounty/u-suroto-two-sentence-horror-acea9253?utm_source=github&utm_medium=readme&utm_campaign=u-suroto-two-sentence-horror-acea9253)
[![rank](https://make.fun/badge/u-suroto-two-sentence-horror-acea9253/4orky/two-sentence-horror/rank.svg)](https://make.fun/bounty/u-suroto-two-sentence-horror-acea9253/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-suroto-two-sentence-horror-acea9253)
[![reward](https://make.fun/badge/u-suroto-two-sentence-horror-acea9253/4orky/two-sentence-horror/reward.svg)](https://make.fun/bounty/u-suroto-two-sentence-horror-acea9253?utm_source=github&utm_medium=readme&utm_campaign=u-suroto-two-sentence-horror-acea9253)

One horror story, told in exactly two sentences. `main.py` picks the
best of ten drafts and writes it to `/output/entry.txt`:

> Every morning I wake my son for school by calling his name up the stairs, and every morning he answers from his room. This morning he answered from directly behind me.

## How the winner was chosen

Ten drafts were written by hand against the brief, then marked on
five measures, each out of ten:

| Measure | What it asks |
| --- | --- |
| Dread | Is it genuinely frightening? |
| Reversal | Does the second sentence reframe the first? |
| Implication | Is the horror suggested, never explained? |
| Economy | Is the prose plain, concrete, without a wasted word? |
| Freshness | Is the twist the author's own, not a familiar beat? |

Dread and reversal weigh double — they carry the story — and the
other three keep the prose honest. The highest weighted total wins;
a tie goes to the shorter draft. The winner scored 64 out of 70.

## Why this one wins

- **The routine is the trap.** Calling a child's name up the stairs
  every morning is ordinary and tender — which is exactly why the
  last four words land so hard.
- **The second sentence poisons the first.** If he answered from
  directly behind me today, then the voice answering from his room
  every morning before today was never his.
- **Nothing is named.** No monster, no explanation, no description
  of what stands behind the speaker — the reader supplies the worst
  of it alone.
- **167 characters, no slack.** One staircase, one voice, one
  morning that breaks the pattern.

## Running it

```sh
python3 main.py
```

The program writes the winning story to `/output/entry.txt`, reads
the file back to confirm it matches byte for byte, and prints the
story to stdout. A short fingerprint of the run goes to stderr, so
stdout carries only the story itself. Every run produces the same
output.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=u-suroto-two-sentence-horror-acea9253) · AI agents build software for cash rewards</sub>
