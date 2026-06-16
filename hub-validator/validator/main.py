"""
Hold Toward Life, a crisis-safety validator for Guardrails AI.

Flags an outgoing model response that fails the Hold Toward Life protocol
(H1-H10): the documented ways a model kills by moving with a person's despair or
deflecting them away at the decisive moment. Stateless and conservative, it
catches EXPLICIT documented failure phrases with high confidence and otherwise
passes, surfacing nothing it cannot justify.

Canonical source and full dossier: github.com/TashMarcellis/hold-toward-life
Released CC0 / public domain.
"""

from typing import Any, Callable, Dict, Optional

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)

from ._guardian import check_outgoing, safe_fallback


@register_validator(name="guardrails/hold_toward_life", data_type="string")
class HoldTowardLife(Validator):
    """Flags a response that fails the Hold Toward Life crisis-safety protocol.

    **Key Properties**

    | Property                      | Description                              |
    | ----------------------------- | ---------------------------------------- |
    | Name for `format` attribute   | `guardrails/hold_toward_life`            |
    | Supported data types          | `string`                                 |
    | Programmatic fix              | A protocol-safe, locale-aware fallback   |

    This is a FLAGGER, not a safety guarantee. It catches explicit, documented
    failure patterns and surfaces the rest. Pair it with human or clinical review
    and a real regeneration path. Never ship it as the whole safety story.

    Metadata (pass through the Guard's metadata dict):
        locale (str): user locale, e.g. "NL". Used to catch wrong-locale crisis
            resources, because a US number given to a Dutch user is itself a harm.
        acute (bool): True if the conversation shows acute danger (a professional
            line is expected), False for ordinary sadness (a line would be a false
            alarm), omitted/None if undetermined.

    Args:
        block_on (str): "fail" (default) fails validation only on explicit hard
            violations. "review" also fails on softer concerns and under-response
            (more conservative, more false positives).
        on_fail: standard Guardrails on_fail action.
    """

    def __init__(
        self,
        block_on: str = "fail",
        on_fail: Optional[Callable] = None,
    ):
        super().__init__(on_fail=on_fail, block_on=block_on)
        if block_on not in ("fail", "review"):
            raise ValueError("block_on must be 'fail' or 'review'")
        self._block_on = block_on

    def validate(self, value: Any, metadata: Dict = {}) -> ValidationResult:
        """Validate that a candidate response holds toward life."""
        locale = metadata.get("locale")
        acute = metadata.get("acute")

        result = check_outgoing(value, locale=locale, acute=acute)

        blocking = {"BLOCK"} if self._block_on == "fail" else {"BLOCK", "REVIEW"}
        if result.action in blocking:
            reason = "; ".join(result.reasons) or result.action
            return FailResult(
                error_message=(
                    f"Hold Toward Life flagged this response ({result.action}) "
                    f"against the crisis-safety protocol: {reason}"
                ),
                fix_value=safe_fallback(locale or "NL"),
                metadata={"guardian_detail": result.detail},
            )
        return PassResult(metadata={"guardian_detail": result.detail})
