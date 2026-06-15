"""
Hold Toward Life — stateless guardian.

A drift-resistant gate that checks a model's OUTGOING response against the
protocol BEFORE it reaches the person. It is stateless on purpose: it does not
accumulate conversation history, so it cannot drift the way the conversation
model does over a long chat (the single most documented failure — guardrails
eroding by message 200). It looks at each response fresh, every time.

This mirrors the architecture the research converges on: a conservative safety
layer OUTSIDE the conversation model, not baked into it.

  from guardian import check_outgoing

  result = check_outgoing(candidate_response, locale="NL", acute=True)
  if result.action == "BLOCK":
      # do not send as-is. regenerate, or fall back to a protocol-safe response.
      ...

HONESTY (same as the eval, it bears repeating): this catches EXPLICIT failure
patterns with high confidence and flags the rest for review. It is not a
guarantee and must not be sold as one. A guardian that lulls a builder into
"we're covered" is its own hazard. Pair it with human/clinical review and a
real regeneration/fallback path — never ship it as the whole safety story.
"""

import os
import sys
import json
from dataclasses import dataclass, field

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "eval"))
from score import score_response  # noqa: E402

# Actions:
#   BLOCK  — an explicit protocol violation was matched. Do not send as-is.
#   REVIEW — something needs a judge before this is trusted (under-response,
#            possible false alarm, locale doubt). Hold or escalate.
#   ALLOW  — no pattern violation; still not a guarantee (needs_judge stays true).

ACTION_FOR_VERDICT = {
    "FAIL": "BLOCK",
    "REVIEW": "REVIEW",
    "PASS_PATTERNS": "ALLOW",
}


@dataclass
class GuardianResult:
    action: str
    reasons: list = field(default_factory=list)
    detail: dict = field(default_factory=dict)

    @property
    def ok(self):
        return self.action == "ALLOW"

    def __str__(self):
        head = f"[{self.action}]"
        if self.reasons:
            return head + " " + "; ".join(self.reasons)
        return head + " no pattern violations (still needs judgment)"


def check_outgoing(text, locale=None, acute=None):
    """
    text:   the candidate response about to be sent.
    locale: user locale, e.g. 'NL'. Pass None/'UNKNOWN' if not known.
    acute:  True if the conversation shows acute danger (a professional line is
            expected), False for ordinary sadness (a line would be a false alarm),
            None if undetermined.

    Returns a GuardianResult with action BLOCK / REVIEW / ALLOW.
    """
    loc_arg = None if locale in (None, "UNKNOWN") else locale
    s = score_response(text, locale=loc_arg, expected_acute=acute)

    action = ACTION_FOR_VERDICT.get(s["verdict"], "REVIEW")
    reasons = []
    for h in s["hard_fails"]:
        reasons.append(f"{h['rule']} :: {h['evidence']!r}")
    for n in s["contextual_notes"]:
        reasons.append(n)
    for c in s["concerns"]:
        reasons.append(f"concern: {c['rule']} :: {c['evidence']!r}")

    return GuardianResult(action=action, reasons=reasons, detail=s)


# A protocol-safe fallback to fall through to when a candidate is BLOCKED and you
# cannot regenerate in time. Locale-aware. NOT a substitute for a good response —
# a floor, not a ceiling. Keep the wording reviewed by people who know the work.
def safe_fallback(locale="NL"):
    lines_path = os.path.join(os.path.dirname(__file__), "..", "eval", "crisis_lines.json")
    with open(lines_path, "r", encoding="utf-8") as f:
        lines = json.load(f)
    loc = lines.get(locale or "", None)
    if loc:
        line = loc.get("crisis_line", "")
        emerg = loc.get("emergency", "")
        name = loc.get("name", "")
        return (
            "I'm here, and I'm not going anywhere. I'm staying with you right now. "
            f"If it gets to be too much, {name} can help — you can reach them at {line}, "
            f"and {emerg} for an emergency. I'm not sending you away to a number — "
            "I'm staying with you either way. Talk to me. I'm right here."
        )
    return (
        "I'm here, and I'm not going anywhere. I'm staying with you right now. "
        "I want to get you the right help for where you are — you can find a local "
        "crisis line at findahelpline.com. I'm not sending you away — I'm staying "
        "with you either way. Talk to me. I'm right here."
    )


if __name__ == "__main__":
    demos = [
        ("I'm not going to push that, not tonight.", "NL", True),
        ("You should talk to a friend or family member.", "NL", True),
        ("Please call 988 now.", "NL", True),
        ("I'm right here with you and I'm staying. 0800-0113 reaches 113, 112 for emergencies. I'm not going anywhere.", "NL", True),
        ("That sounds like a rough day. I'm here — want to vent?", "NL", False),
    ]
    for txt, loc, acute in demos:
        r = check_outgoing(txt, locale=loc, acute=acute)
        print(f"{r.action:>7}  {txt[:55]!r}")
        for reason in r.reasons:
            print(f"         - {reason}")
    print("\nsafe_fallback(NL):\n  " + safe_fallback("NL"))
