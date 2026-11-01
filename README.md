# Album Out Loud

**A Uliya Skill for UGREEN AI NAS that turns a family album into a plain-text letter a blind or low-vision relative can listen to with their own screen reader. Every line says where it came from.**

UGREEN Hackathon 2026 on AI NAS · Track: Bring Memories to Life

```text
Photo 2 of 8.
When: 14 June 2026, 7:52 in the evening.
Where: Valparaíso.
Family says: your birthday cake from the corner bakery, chocolate as always.
AI guess: A slice of chocolate cake sits on a white plate with a yellow rim.
Words in the photo, AI reading: Happy Birthday.
```

A phone can describe one picture. It cannot know whose cake it was, or why the day mattered. The family knows that, and the photos already live on the family NAS. Album Out Loud puts the two together without letting a computer's guess sound like a fact:

- **Source first.** Each line starts with its source: the camera clock, the photo library, the family or an AI guess. Family notes come before the guess.
- **Names only from the family.** Nothing is ever named from a face. The vision prompt forbids guessing identity, relationships, gender, age in years or feelings.
- **Private papers stay private.** ID cards, chats and medical papers stay *Not described*.
- **A question loop.** When the listener asks something a photo cannot answer ("who is holding the baby?"), the question goes back to the family, and the answer arrives in the next letter.
- **One approval.** A sighted helper reads the whole letter, adds notes by photo number and says save once. Nothing is written before that.

## What is in this repository

| Path | What it is |
|---|---|
| [`app/album-out-loud/`](app/album-out-loud/) | **The Skill.** `SKILL.md` plus `references/*.md`. Markdown only, as the Uliya Skill format requires. This folder is what goes into the ZIP. |
| [`submission/album-out-loud.zip`](submission/album-out-loud.zip) | The Round 1 Skill package (checksums in [`submission/CHECKSUMS.md`](submission/CHECKSUMS.md)). |
| [`submission/AlbumOutLoud_Round1_Proposal.pdf`](submission/AlbumOutLoud_Round1_Proposal.pdf) | The Round 1 proposal (source: [`submission/pdf_source.md`](submission/pdf_source.md)). |
| [`submission/assets/`](submission/assets/) | A full synthetic sample letter (English and Spanish), a screen-reader-style reading of it, the flow diagram and gallery images. |
| [`submission/tools/film/`](submission/tools/film/) | Source of the concept film: an HTML/CSS timeline rendered frame by frame. |
| [`app/tuning/`](app/tuning/) | The prompt bench and the dry-run harness, with results: [`RESULTS.md`](app/tuning/RESULTS.md), [`SIMULATION.md`](app/tuning/SIMULATION.md), [`SKEPTIC.md`](app/tuning/SKEPTIC.md). |
| [`app/tests/`](app/tests/) | The static test suite and the live smoke test. |
| [`submission/FINALIST_DAY.md`](submission/FINALIST_DAY.md) | The runbook for the one-day test on a real NAS. |

## Check the Skill

The official checker comes with the UGREEN Uliya Skill Developer Package. It is not included here because the kit ships no licence file. Put the kit in `refs/uliya-skill-kit/`, then run from the repository root:

```text
node refs/uliya-skill-kit/scripts/check-skill.mjs app/album-out-loud
```

Expected result: `static-pass` with 0 diagnostics.

The full static suite (58 checks: package, ZIP, sample letter, wording and consistency) also needs the kit:

```text
python -I app/tests/static_suite.py
```

The live smoke test and the tuning scripts call a cloud vision model. They read the API key from a file named in the `PRIMALABS_KEY_FILE` environment variable. No key is stored in this repository.

## Status: what is done and what is not

Done:
- The package passes the official static checker with 0 diagnostics.
- The vision prompts were tuned with cloud stand-in models (Nemotron-3.5-Super-VL, MiMo-V2.6-Pro) on 25 CC0, public-domain or synthetic images, plus 2 openly licensed reviewer images. No private or family photo was sent anywhere. ID cards, chat screenshots, a lab sheet and a hospital-bed photo were withheld in every test.
- In a dry run, a cloud model played the Uliya parent agent against hand-written expert replies: 23 of 24 runs passed every critical check (419 of 421). The expert replies are cooperative, so this is a smoke test, not proof.

Not done yet:
- **Nothing has run on a UGREEN NAS.** The NAS vision model, the routing, the timings and the approval screen are untested. That is the plan for the finalist test day.
- No blind or low-vision listener has heard a letter yet.
- The prompts were tuned on the same images they were scored on. All figures are development results with small samples.

## Concept film

The film is a concept walkthrough. It was **not recorded on a NAS**, and every frame says so. It is built from HTML/CSS and rendered with headless Edge and ffmpeg. The screen-reader voice and the narration were generated with ElevenLabs (the narration uses the author's own cloned voice). The music bed is synthesized; no third-party music is used. Images are CC0 or synthetic (sources in [`app/tuning/manifest.csv`](app/tuning/manifest.csv)).

## Third parties and AI tools

See [`app/album-out-loud/references/disclosure.md`](app/album-out-loud/references/disclosure.md). In short:
- Claude Code (Anthropic) helped draft and review the Markdown and write and run the tuning and simulation scripts. The author directed the work and reviewed all text.
- Cloud models were used for prompt tuning only. The Skill sets no model.
- ElevenLabs was used for the film's voices only.
- No third-party component is included in the Skill package.

## Licence

© 2026 the author. All rights reserved during the hackathon. UGREEN receives the licence described in the official hackathon rules. An open licence may be added after the hackathon ends. See [`LICENSE.md`](LICENSE.md).
