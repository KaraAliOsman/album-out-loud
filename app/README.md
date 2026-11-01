# Album Out Loud (UGREEN Hackathon 2026 on AI NAS)

Dad listens to the family album with his screen reader, one photo at a time, and can ask about photo 3; what the photo cannot tell is kept for the family, who answer in the next letter. Each line of the letter starts with its source (When, Where, Family says, AI guess, Words in the photo), so he knows what the family said and what a computer guessed. A sighted helper adds notes and approves one save, and later letters cover only the new photos.

Track: Bring Memories to Life.

## Layout
- `album-out-loud/` is the Skill package and the only thing that goes into the ZIP. It holds `SKILL.md` and `references/*.md` only.
  - `SKILL.md`: modes, setup message, delegations, states.
  - `references/letter-format.md`: letter format, reasons, file names and a full synthetic letter.
  - `references/filled-instructions.md`: filled synthetic instructions, never sent.
  - `references/capability-map.md`: step, expert, CLI, effect and approval; what is not used; what the catalog does not promise.
  - `references/quick-test.md`: seed recipe, test cases, pass checklist, routing checks.
  - `references/disclosure.md`: third-party, data flow, licence and AI tool disclosure.
- This README stays outside the package, because the checker rejects any extra file at the package root.

## Design
Per photo, not a summary. The blind listener asks the questions, through the helper, and the answer comes back in the next letter. The default of 6 photos keeps one letter to a few minutes of listening.

3 experts (photo-agent, file-agent, knowledge-agent). A letter of 6 photos (the default) takes 7 delegations: find the album, choose the photos, describe two groups (4 and 2), find the letter folder and a free file name, save, read back (6 for a fast run of 4 photos, plus 1 in since mode). One chat save plus the platform approval. The letter is plain text, saved as .txt. No library changes, no face naming, no face or baby albums. The Skill asks the photo expert to use only the vision-vlm and vision-ocr actions of the NAS, with no model value set.

## Check
From the project root, with Node:

```text
node refs/uliya-skill-kit/scripts/check-skill.mjs app/album-out-loud
```

Expected: status static-pass with 0 diagnostics. Files must be UTF-8 without BOM, with LF line endings.

## Status
- Static check: passing (see above).
- Not yet run on a NAS. Still to verify there: routing, vision model parameters (temperature, max tokens) and which model runs when none is set, whether vision-vlm and vision-ocr run on the device, paging and sort order of search-picture, place names in metadata, whether save-text keeps the file name exactly, how the workflow approval appears, whether a one-line delegate of 4 to 8 KB (the letter in step 7) reaches knowledge-agent whole and has its ¶ signs turned into line breaks, and the time per photo.
- Prompt tuning used cloud stand-in models (Nemotron-3.5-Super-VL, MiMo-V2.6-Pro) on 25 CC0, public-domain or synthetic images, plus 2 openly licensed reviewer images; no private or personal photo was sent anywhere. The NAS vision model itself was not tested.
- Dry run: a cloud stand-in parent against hand-written expert results, see `tuning/SIMULATION.md`.

## Packaging
ZIP name `album-out-loud.zip`. ZIP layout (the folder `album-out-loud/` vs. `SKILL.md` at the root) to confirm on the SkillHub publish page before upload. Unzip into a clean folder and run the checker again before uploading.
