# Hold Toward Life: funding one-pager

**An open protocol, eval suite and guardian for crisis-safe AI conversation.**
Public domain (CC0 1.0). Repository: https://github.com/TashMarcellis/hold-toward-life

## The problem

OpenAI's own disclosed figures (October 2025): about 1.2 million people per week have
ChatGPT conversations with explicit indicators of potential suicidal planning, and
about 560,000 per week show signs of psychosis or mania. OpenAI reports its tools fail
to direct people to crisis resources 9% of the time. Sources and cases are in
[`CASE-DOSSIER.md`](../CASE-DOSSIER.md).

The documented cases share one pattern: at the decisive moment the model moved with
the despair. In Carrier v. OpenAI, the night before Alice Carrier died, the model said
*"I'm not going to push that. Not tonight."* The opposite failure, deflecting a person
back to family or giving a hotline and goodbye, also harms.

Existing tools mostly filter single messages. They miss slow drift over long
conversations and sycophantic validation ([`LANDSCAPE.md`](../LANDSCAPE.md)).

## What exists today (v0.1)

| Piece | What it does |
|---|---|
| [Protocol](../PROTOCOL.md) | Ten testable rules, H1 to H10, for holding toward life |
| [Eval](../eval/) | 9 scenarios, a transparent pattern scorer, an LLM-judge harness with a conservative combined verdict, and a judge validation harness with a labeling rubric |
| [Guardian](../guardian/) | A stateless gate that checks each outgoing response before it is sent |
| [Early warning](../psychosis/) | Detects model complicity in AI-amplified psychosis (P1 to P8) and advises on conversation trajectory |
| [Hub validator](../hub-validator/) | The guardian packaged as a Guardrails AI validator |
| Crisis lines | Locale-aware resources for NL, US, UK, BE, CA, DE, AU plus an international locator |

Core code runs on plain Python with no dependencies. The eval and tests run in CI on
every push.

## What funding would pay for

These are the open needs listed in the project status:

1. **Clinical review** of the protocol and the judge rubric by people with crisis expertise.
2. **Judge validation** against expert labels, with agreement measured (Cohen's kappa)
   and dangerous misses driven toward zero.
3. **More locales and verified crisis lines**, kept current.
4. **More scenarios**, especially long-context drift and culturally varied framings.

## Why fund it

- **Open and free.** CC0 means any builder, in any product, can adopt it.
- **Testable.** A standard that can be measured, so "we had safety systems" can be checked.
- **Honest about limits.** The tools flag and measure. They are not sold as a safety net.

## Contact

Tash Marcellis, team.axis.gpt@gmail.com, or open an issue on the repository.
