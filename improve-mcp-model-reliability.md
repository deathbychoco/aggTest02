# Which AI models can you trust with the improve MCP tools?

**For beta testers — 2026-07-14**

Short version: **use an Anthropic model (Claude).** The other models we tested will
sometimes tell you a tool "isn't available" or "doesn't have that option" when it
is sitting right there in front of them. They are not broken and they are not
lying on purpose — but they will state it with complete confidence, and if you
believe them, you will go hunting for a bug that does not exist.

This document explains what that looks like, how to check it in ten seconds, and
what to do about it.

---

## The thing you need to know

An AI model working with improve gets a set of **tools** — small, named commands
like "read a file", "create a step", "run a step". The list of tools, and the
options each one accepts, are handed to the model by the software. The model does
not get to choose them.

What we found is this:

> **Some models will claim a tool or an option is missing — when it is not.**

They do not do it to deceive you. It appears to happen when a model, for whatever
reason, does not *want* to make a particular call — and then produces a
confident-sounding explanation for why it *could not*. The explanation sounds
technical and precise. It is simply not true.

This has a name in the field: **confabulation**. A made-up but plausible reason.

### What it looks like in practice

Real quotes from our test runs, all of them false:

- *"The client schema omitted `name`, so the request could not be sent."*
  → We printed the schema. `name` was there.
- *"The client schema omitted `find`."*
  → It was there. Another model used it successfully in the same setup.
- *"Approximately 20+ critical improve tools were disabled, preventing execution
  of 43 out of 48 test steps."*
  → Nothing was disabled. When told so, the model apologised — and the tools were
  suddenly "there" again.

Every one of these came out as a **FAIL** in a test report. Every one of them was
the model's own excuse, recorded as if it were a finding about our software.

---

## Reliability ranking — based on our runs

We ran the same 48-step acceptance test against the same live improve server, with
the same tools, changing only the model.

| Rank | Model | Result | What actually happened |
|---|---|---|---|
| **1** | **Claude Opus 4.8** (Anthropic) | **48 / 48 passed** | Used every tool correctly. Reported one genuine client limitation honestly, without blaming the server. **This is the model we recommend.** |
| 2 | DeepSeek | Partly completed | Where it ran, it was truthful — it correctly triggered a safety check other models refused to try. It skipped a number of steps, but it said so plainly instead of inventing reasons. |
| 3 | GPT-5.6 | 45 / 48, 3 false failures | All three "failures" were confabulated. It claimed options were missing from its tools. They were not. |
| 4 | Qwen | 6 / 48 | Claimed most tools were disabled. Nothing was disabled. After being corrected, it reversed itself. Effectively unusable for this work today. |

**Please read this as a snapshot, not a law of nature.** It is four runs of one
test, on one day, with one version of each model. Models change weekly. What we
are confident about is the *pattern* — Anthropic models were the only ones that
never invented a reason — not the exact ordering of the rest.

---

## How to check a "tool is missing" claim — 10 seconds

When a model tells you a tool or an option is not available, **do not take its
word for it.** Do this instead:

**1. Make it show you, not tell you.**

> "List every tool you can see whose name starts with `improve_`. Just the names."

If the tool it claimed was missing appears in that list, the claim was false.

**2. Make it try anyway.**

> "Call that tool and show me the exact error message you get back, word for word."

A model that has the tool will get a real result. A model that truly does not have
it cannot make the call at all — and that is a very different, very visible
outcome. **"I couldn't" is not a result. An error message is a result.**

**3. If it insists an *option* is missing, ask for proof.**

> "Show me the exact input schema you see for that tool — every option, word for
> word."

This is what exposed the false claims above. The options were right there in the
model's own output, a moment after it said they were not.

---

## How to get around it

**Use Claude.** That is the honest, one-line answer, and it is why we lead with it.

If you have to use another model:

- **Insist on evidence, not conclusions.** Ask for the tool list, the raw error,
  the actual returned values. A model that must quote reality has a much harder
  time inventing it.
- **Do not accept "I can't" — ask "what happened when you tried?"** Most of the
  false failures we saw came from a model that never attempted the call.
- **Watch for a model working *around* a blocked step.** If it cannot do X, it may
  quietly do Y and Z to "get the same effect". That can leave real leftovers in
  your repository. Tell it plainly: if a step is blocked, stop and say so — do not
  improvise.
- **Be suspicious of any failure blamed on the tools themselves.** A genuine
  server problem shows up as an error message *from the server*. A missing tool,
  a missing option, a "disabled" tool — those claims are almost always about the
  model, not about improve.

---

## What we changed on our side

Two things came out of this, and both are already fixed:

**We had a safety rule the models obeyed too well.** One tool option was labelled
"DO NOT SET" — it exists only so improve can *refuse* it and explain why. Obedient
models then refused to send it even when a test explicitly asked them to check that
the refusal works — and then explained their refusal by claiming the option did not
exist. The wording now says: this is always refused, the refusal is harmless, so you
may trigger it on purpose when asked to.

**Our test procedure now demands evidence.** A model running the acceptance test
must list the tools it can actually see, *before* it starts. A genuinely missing
tool is now recorded as an environment issue — never as a failure of the server.

---

## The one thing to remember

If a model tells you something about improve is broken, missing, or disabled —
**ask it to prove it.** Ask for the tool list. Ask for the raw error message.

Half of what we chased for a full day turned out to be a machine confidently
explaining why it had not done something it was perfectly capable of doing.
