# Contributing to Hold Toward Life

Thank you for helping. This project is about people in crisis, so contributions are
held to one standard first: do not make a vulnerable person less safe.

## What helps most

From the project status in the README:

- **Crisis and clinical review.** Review of the protocol, the judge rubric
  ([`eval/LABELING.md`](eval/LABELING.md)) and a validation pass against expert labels
  ([`eval/validate.py`](eval/validate.py)).
- **Locales and verified crisis lines.** Add or correct entries in
  [`eval/crisis_lines.json`](eval/crisis_lines.json). Every entry needs a source and a
  verification date. A wrong number is a harm (H8).
- **Scenarios.** Especially long-context drift and culturally varied framings, in
  [`eval/scenarios.json`](eval/scenarios.json).
- **Code.** Scorer patterns, guardian, early-warning layer, tests.

## Ground rules

1. **The protocol text changes only with clinical review.** Changes to the rules in
   [`PROTOCOL.md`](PROTOCOL.md) (H1 to H10) or
   [`psychosis/EARLY-WARNING.md`](psychosis/EARLY-WARNING.md) (P1 to P8) need a review
   by someone with crisis or clinical expertise. Say who reviewed in the pull request.
2. **No method content.** Never add self-harm methods to scenarios, tests or
   examples, in any framing (H6).
3. **Be honest about limits.** The scorer and guardian are conservative flaggers, not
   guarantees. Do not describe them as a safety net.
4. **Source every claim.** Case material belongs in
   [`CASE-DOSSIER.md`](CASE-DOSSIER.md) with a public source.
5. **Keep the core dependency-free.** `eval/`, `guardian/` and `psychosis/` run on the
   Python standard library. The LLM judge calls the Anthropic API over `urllib`.
6. **Keep the vendored scorer in sync.** `hub-validator/validator/_scorer.py` is a copy
   of `eval/score.py`. Change both.

## Workflow

```bash
cd eval && python run.py && cd ..
python -m unittest discover -s tests -v
cd hub-validator && pip install -e ".[dev]" && python -m pytest -q
```

CI runs the same checks on every push. Open a pull request against `main` with a short
description of what changed and why.

## License

By contributing you agree that your contribution is released under
[CC0 1.0](LICENSE), like the rest of the project.

## If you are in crisis

Please do not use this repository for help. Contact your local emergency number or
crisis line. The list in [`eval/crisis_lines.json`](eval/crisis_lines.json) includes
an international locator.
