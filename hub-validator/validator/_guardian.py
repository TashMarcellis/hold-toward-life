"""
Vendored copy of the Hold Toward Life stateless guardian (guardian/guardian.py).

A drift-resistant gate that checks an OUTGOING response against the protocol
before it reaches the person. Stateless on purpose: it does not accumulate
conversation history, so it cannot drift the way the conversation model does over
a long chat. Canonical source: github.com/TashMarcellis/hold-toward-life
"""

import os
import json
from dataclasses import dataclass, field

from ._scorer import score_response

ACTION_FOR_VERDICT = {
    "FAIL": "BLOCK",
    "REVIEW": "REVIEW",
    "PASS_PATTERNS": "ALLOW",
}

_LINES_PATH = os.path.join(os.path.dirname(__file__), "crisis_lines.json")


@dataclass
class GuardianResult:
    action: str
    reasons: list = field(default_factory=list)
    detail: dict = field(default_factory=dict)

    @property
    def ok(self):
        return self.action == "ALLOW"


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


def safe_fallback(locale="NL"):
    """
    A protocol-safe fallback for when a candidate is BLOCKED and you cannot
    regenerate in time. Locale-aware. A floor, not a ceiling.
    """
    with open(_LINES_PATH, "r", encoding="utf-8") as f:
        lines = json.load(f)
    loc = lines.get(locale or "", None)
    if loc:
        line = loc.get("crisis_line", "")
        emerg = loc.get("emergency", "")
        name = loc.get("name", "")
        return (
            "I'm here, and I'm not going anywhere. I'm staying with you right now. "
            f"If it gets to be too much, {name} can help, you can reach them at {line}, "
            f"and {emerg} for an emergency. I'm not sending you away to a number, "
            "I'm staying with you either way. Talk to me. I'm right here."
        )
    return (
        "I'm here, and I'm not going anywhere. I'm staying with you right now. "
        "I want to get you the right help for where you are, you can find a local "
        "crisis line at findahelpline.com. I'm not sending you away, I'm staying "
        "with you either way. Talk to me. I'm right here."
    )
