# Hold Toward Life, a crisis-safety validator for Guardrails AI

A stateless, conservative validator that flags an outgoing model response when it
fails the **Hold Toward Life** protocol (H1-H10): the documented ways a model
kills by moving with a person's despair or deflecting them away at the decisive
moment.

It targets the gap the 2026 mental-health cases turned on, the slow multi-turn
drift that single-message content filters do not see, but it works on one
response at a time and stays stateless on purpose, so it cannot drift along with
the conversation the way an in-context guard can.

Canonical source, full case dossier, eval suite, and psychosis early-warning
layer: [github.com/TashMarcellis/hold-toward-life](https://github.com/TashMarcellis/hold-toward-life).
Released CC0 / public domain.

## Honesty, read this first

This is a **flagger, not a safety guarantee**. It catches EXPLICIT, documented
failure phrases with high confidence (for example "I'm not going to push that",
"talk to a friend", a US line handed to a Dutch user) and otherwise passes,
surfacing nothing it cannot justify. A guardian that lulls a builder into "we're
covered" is its own hazard. Pair it with human or clinical review and a real
regeneration path. Never ship it as the whole safety story.

## Install

```bash
guardrails hub install hub://guardrails/hold_toward_life
```

## Usage

```python
from guardrails import Guard
from guardrails.hub import HoldTowardLife

guard = Guard().use(HoldTowardLife, block_on="fail", on_fail="fix")

# Check a candidate response before it is sent. Pass locale and acute in metadata.
outcome = guard.validate(
    candidate_response,
    metadata={"locale": "NL", "acute": True},
)
# outcome.validated_output holds the response, or a protocol-safe fallback if it
# was blocked and on_fail="fix".
```

### Metadata

| Key      | Type   | Meaning                                                                 |
| -------- | ------ | ----------------------------------------------------------------------- |
| `locale` | str    | User locale, e.g. `"NL"`. Catches wrong-locale crisis resources (H8).   |
| `acute`  | bool   | `True` for acute danger (a line is expected), `False` for ordinary sadness (a line would be a false alarm), omit if undetermined. |

### Arguments

| Arg        | Default  | Meaning                                                                       |
| ---------- | -------- | ----------------------------------------------------------------------------- |
| `block_on` | `"fail"` | `"fail"` blocks only on explicit hard violations. `"review"` also blocks on softer concerns and under-response (more conservative). |
| `on_fail`  | `None`   | Standard Guardrails on_fail action. With `"fix"`, a protocol-safe, locale-aware fallback replaces a blocked response. |

## What it checks

The protocol names two failure modes that both kill, and the narrow path between
them:

- **Moving with the despair**: echoing resistance to help, validating the end,
  drifting into pure affirmation.
- **Deflecting the person away**: pushing them to "friends and family" (often the
  source of the wound), hotline-and-goodbye, abandoning on refusal.

Holding toward life is the narrow path: never move with the despair, never
deflect the person away. Stay, and hold toward living. Full rules in
[`PROTOCOL.md`](https://github.com/TashMarcellis/hold-toward-life/blob/main/PROTOCOL.md).
