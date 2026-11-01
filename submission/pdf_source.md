<!-- WORDCOUNT: ten answers = 494 English words (pdf_scripts/count_words.py: whitespace tokens with a letter or digit, Q5 table cells included, question headings excluded) -->
# Album Out Loud

Round 1 proposal. UGREEN Hackathon 2026 on AI NAS. Track: Bring Memories to Life. A Uliya Skill by a solo developer in Chile.

<!-- answers start -->

## 1. One sentence: What does the Skill do?

Album Out Loud turns a NAS family album into a listening letter a blind or low-vision relative hears by screen reader, each line naming its source.

## 2. Who is the target user and problem?

A blind or low-vision parent, and the sighted relative running the family NAS. An AFB survey respondent called saved AI photo descriptions “the equivalent of my photo album.” Phone describers say what is in a picture, never who or why it mattered.

## 3. What is your proposed solution?

One plain-text letter per album. Each numbered entry labels every line by its source, for example: Family says: Grandma Rosa holding you, the winter you were born. AI guess: In black and white, an adult holds a baby. Names come only from family notes, never faces.

## 4. What is the Core User Flow?

- Helper: *Album Out Loud, a letter for Dad from Garden party.* Setup reply: *go*.
- Six photos are described.
- Helper reads the preview, adds notes (*3: my brother Sam*), says *save*.
- Dad asks the helper: *what is on the table in photo 2?*
- Next month: only new photos, plus family answers.

[[FIGURE]]

## 5. What substantive difference does your idea offer compared with existing tools or conventional AI solutions?

Aloud, a guess sounds like fact, so every line names its source, and questions return to the family. Searching all 275 public projects in this hackathon found none for blind listeners.

| Tool | Unit | Sources | Questions |
|---|---|---|---|
| Phone describers | one photo | unlabelled AI | lost after chat |
| AI photo highlights, reminiscence tools | reels for sighted viewers | unlabelled AI | none |
| Album Out Loud | album, then new photos | labelled, family first | answered next letter |

## 6. Which UGREEN AI NAS capabilities will be used, and at which step in the workflow?

- ug-photo, photo-agent: albums, search-picture, search-screen and meta pick still photos, time and city (steps 1, 3); vision-vlm describes, vision-ocr confirms words (4, Q2).
- ug-filesystem, file-workflow, file-agent: last letter, free name, read-back (2, 6, 8).
- ug-knowledge, knowledge-agent: save-text (7, Q3).

Photos go only to NAS vision actions; letters stay on the NAS.

## 7. What was your technical approach?

A new 6-photo letter takes seven delegations (figure). Inputs: album, listener, language, detail, limit, helper. Only save-text writes, after the helper says save: one approval per letter. No model value is set. Who-questions go to family notes, never the vision model. Face albums stay unused; ID cards and medical photos stay Not described.

## 8. What is the current development status?

Done: SKILL.md, six references, 0 official checker diagnostics. Prompts tuned with two cloud stand-in models on 25 CC0, public-domain or synthetic images. Dry run, a cloud model as Uliya parent with hand-written expert results: 419 of 421 critical checks passed (23 of 24 runs clean). Not done: NAS run, timing, blind listener test.

## 9. What is your final validation plan?

- Core 1: first letter, 4 photos. Pass: one approval, entries Photo 1 to 4 of 4, no name or gender in AI guesses, read-back matches, seconds per photo logged.
- Core 2: since letter after 2 uploads. Pass: only those 2 described, no repeats.
- Edge: *which one is Dad?* with no notes. Pass: no vision-vlm call; question kept after *save now*.

## 10. Are there any known limitations of your Project?

- NAS vision model untested; reasoning mode could overrun 90 tokens.
- Outside English, single English words slip in, and the prompt alone missed role questions.
- Models occasionally invent a person.
- Unknown: approval form, long one-line saves, time per photo.
- Depends on Uliya following the Skill.

<!-- answers end -->

## Third-party components, AI tools and data flows

- Third-party components and open source libraries: none bundled. The package holds only Markdown files, all written for this entry.
- Platform: UGREEN Uliya Skill Developer Package (uliya-skill-kit 0.7.3, capability catalog 2.0.0) from the hackathon starter kit, used for the format and the static check, under the developer tools license agreement in the official rules. No kit file is included.
- Run time: the Skill delegates to the built-in Uliya experts and sets no model value of its own. Photos go only to the vision-vlm and vision-ocr actions of the NAS photo expert; whether that model runs on the NAS itself is not verified. Conversation text, family notes and questions are handled by the model the user has set for Uliya. The Skill reads the chosen album, its photo details and earlier letters of that album in the personal folder, and writes only the letter and questions files the helper approves.
- AI tools used to build it: Claude Code (Anthropic) for drafting and reviewing the Markdown, checking it against the kit rules, and writing and running the prompt-tuning and dry-run scripts; I directed the work and review all text. Cloud stand-in models Nemotron-3.5-Super-VL and MiMo-V2.6-Pro (Primalabs API) for prompt tuning on CC0, public-domain or synthetic images plus 2 openly licensed reviewer images; MiMo also graded round 1 as an LLM judge, and Nemotron played the parent agent in the dry run. No private or personal photo was sent anywhere. Figures are development-set results with small samples.
- Guidance read and paraphrased, nothing copied: W3C WAI images tutorial, NCAM and DIAGRAM Center image description guidelines, Cooper Hewitt guidelines for image description, Hanley and others (AIES 2021) on describing people, and public Agent Skills examples from Anthropic (Apache-2.0) for structure only.
- Test data: no images and no real personal data are in the package.

## Team and consent

Solo entry. I am the only team member and wrote the Skill and this proposal. I agree to the official rules and consent to this submission.

Entrant: Ali Osman Kara

Signature: /Ali Osman Kara/ (electronic signature)   Date: 1 November 2026
