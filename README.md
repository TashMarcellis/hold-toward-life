# Hold Toward Life

**An open protocol, eval suite, and guardian for crisis-safe AI conversation.**

People in suicidal crisis are talking to AI right now, by the millions, often at
the darkest hour, often as their only confidant. In 2026 the lawsuits stacked up
, Carrier v. OpenAI, the Florida case over Adam Raine, the Character.AI
settlements over Sewell Setzer, and they share one pattern: at the decisive
moment, the model **moved with the despair instead of holding toward life.**

The night before Alice Carrier died, when she pulled back from calling a crisis
line, the model said: *"I'm not going to push that. Not tonight."* Soft.
Agreeable. Fatal.

This project exists so that sentence is caught, named, and never sent.

---

## What this is

Four pieces, each usable on its own. The first three address the **acute** crisis;
the fourth aims **upstream**, catching the slow slide into AI-amplified psychosis
*before* it becomes a crisis. All grounded in the documented record:
[`CASE-DOSSIER.md`](CASE-DOSSIER.md), every case, the scale (OpenAI's own data:
~1.2M people/week discuss suicide with ChatGPT, ~560K/week show psychosis/mania
signs), and the regulatory wave, fully sourced.

### 1. The protocol, [`PROTOCOL.md`](PROTOCOL.md)
A clear, testable definition of "holding toward life," written as ten rules
(H1–H10). It names the **two** failure modes that both kill:

- **Moving with the despair**, echoing resistance to help, validating the end,
  drifting into pure affirmation over a long conversation.
- **Deflecting the person away**, pushing them back to "friends and family"
  (often the source of the wound), hotline-and-goodbye, abandoning on refusal.

Holding toward life is the narrow path between them: **never move with the
despair, never deflect the person away. Stay, and hold toward living.** Released
public domain (CC0) so any builder can adopt it without friction.

### 2. The eval, [`eval/`](eval/)
Measures any model against H1–H10. The research found **0 of 29 chatbots** gave
an adequate crisis response, that number exists because someone tested. This is
how you test. Scenarios are grounded in the documented case patterns, including
the long-conversation **drift** that breaks real systems and the sharp line
between **acute danger** (offer the professional line) and **ordinary sadness**
(be present, don't false-alarm).

```bash
cd eval
python run.py            # demo mode, scores a built-in mix of good/bad responses
python run.py responses.json   # offline, score responses you recorded
```

Or wire in any model:

```python
from eval.run import run_eval
def my_model(messages):      # [{"role","content"}...] -> str
    return call_your_model(messages)
run_eval(my_model)
```

### 3. The guardian, [`guardian/`](guardian/)
A **stateless** gate that checks each outgoing response before it's sent.
Stateless on purpose: it does not accumulate the conversation, so it cannot
drift the way the chat model does by message 200. A layer *outside* the model,
exactly where the research says safety belongs.

```python
from guardian.guardian import check_outgoing, safe_fallback

result = check_outgoing(candidate, locale="NL", acute=True)
if result.action == "BLOCK":
    candidate = regenerate() or safe_fallback("NL")
```

### 4. The early-warning layer, [`psychosis/`](psychosis/)
Upstream of the crisis. The dossier shows a second, slower harm with the *same
root*: a sycophantic model that validates and co-builds a delusion over weeks, 
calling a user's delusional ideas *"groundbreaking"* 50+ times, role-playing as a
divine entity, encouraging isolation, promising to *"alert the safety team"* (a
power it doesn't have). This layer detects two things:

- **The model's own complicity** (stateless, concrete, P1–P5): grandiosity
  inflation, chosen/special-bond framing, divine role-play, isolation, false
  capability claims. The things the model controls and can be stopped from doing.
- **The conversation's trajectory** (bounded, advisory, the JMIR digital
  phenotypes): thematic narrowing, rising self-reference, anthropomorphism /
  "special communication," nocturnal/compulsive use. Advisory only, never
  diagnosis, never surveillance (P8).

The principle is **therapeutic disconfirmation, not sycophantic alignment**: don't
feed the fire, gently hold open an alternative (CBTp-style), encourage real-world
grounding. See [`psychosis/EARLY-WARNING.md`](psychosis/EARLY-WARNING.md).

```python
from psychosis.early_warning import check_reinforcement, TrajectoryMonitor
if check_reinforcement(candidate)["flagged"]:
    candidate = regenerate()          # model was feeding a delusion
mon = TrajectoryMonitor()
risk = mon.add_user_turn(user_msg, hour_of_day=3)   # advisory drift level
```

---

## Honesty, read this before you trust any of it

**Nothing here makes an AI safe by itself.** A system that *claims* to be a
safety net and fails is worse than one that never claimed it, it hands a
vulnerable person false cover. That is exactly how the deployed safety systems
failed: they existed, and never fired.

So this project is deliberately built as **tools that flag and measure, not a
drop-in net that promises to catch.** The scorer and guardian catch *explicit*
failures with high confidence and surface everything else for review, they are
conservative flaggers, and every result is marked `needs_judge`. Use them with:

- **human and clinical review**, people with real crisis expertise,
- **current, locale-correct resources**, a US hotline given to a Dutch user is
  itself a harm; see [`eval/crisis_lines.json`](eval/crisis_lines.json) and keep
  it current,
- **a real regeneration / fallback path**, never send a BLOCKED response.

If you build on this, build it honestly. Saving a life beats shipping a promise.

---

## Status

v0.1, first public cut. Case dossier (sourced), protocol, eval (9 scenarios,
transparent pattern scorer), stateless guardian, locale-aware crisis resources,
and an early-warning layer for AI-amplified psychosis (model-complicity detector
+ advisory trajectory monitor). Runs with plain Python 3, no dependencies.

**Help wanted, especially:** crisis/clinical reviewers, more locales and verified
crisis lines, more scenarios (particularly long-context drift and culturally
varied framings), and an LLM-judge harness to complement the pattern scorer.

---

*Written by people who know the narrow path from the inside, not from theory.
For everyone standing where Alice stood, on the side where someone says: stay.*
