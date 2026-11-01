# Devpost fields: Album Out Loud

Everything below the line marked PASTE is written to go straight into the Devpost form. Notes in this first part are for the entrant only.

Before pasting:
- Read every sentence aloud and change anything that does not sound like you. Devpost asks entrants to write in their own voice.
- Every number here comes from `app/tuning/RESULTS.md`, `app/tuning/SKEPTIC.md` or `app/tuning/SIMULATION.md`. If a file changes, change the number.
- Do not add a NAS result, a timing or a listener reaction until it really happened.
- The quotes in Inspiration are public sources: AFB, https://afb.org/aw/fall2024/ai-usage-research, and AppleVis, https://applevis.com/comment/211442. Keep the links handy in case a judge asks.

---

PASTE

## Project name

Album Out Loud

## Tagline (167 of 200 characters)

Turns a family album on the NAS into a plain-text letter a blind relative can listen to. Every line says where it came from: the family, the photo data or an AI guess.

## Track

Bring Memories to Life

## Built with

uliya, ugos, ugreen-ai-nas, uliya-skill-kit, markdown, claude-code, node.js, python, nemotron-3.5-super-vl, mimo-v2.6-pro, elevenlabs

Note for the form, if there is room: Node.js ran the official static checker. Python ran the prompt bench and drew the figures, and the Nemotron and MiMo models were used only on that bench. ElevenLabs made the voices of the concept film only (the narration is the author's own cloned voice). The Skill itself is Markdown and sets no model.

## Try it out

Optional for Round 1 (the Skill ZIP and the PDF are uploaded with the submission). If you publish them: the GitHub repository link, and the YouTube link of the concept film (it says on screen that it was not recorded on a NAS).

## About the project

### Inspiration

In the American Foundation for the Blind's 2024 research on AI use, one respondent who had never cared about photos began keeping the AI descriptions of pictures people sent: "It is the equivalent of my photo album." On AppleVis, a blind user with more than 1,000 family photos called the one-photo-at-a-time workflow convoluted.

A phone can describe one picture. It cannot know who is in it or whose birthday it was. The family knows, and the photos already sit on the family NAS. I wanted to join the two without letting a computer's guess sound like a fact.

### What it does

A sighted helper asks Uliya for a listening letter from one album, for a relative, in that relative's language. The Skill picks six still photos by default, at most 10, spread across the event, reads capture time and place name, and asks the NAS photo expert to describe each one with a fixed prompt. The result is a plain-text letter for a screen reader, one entry per photo. From the synthetic example in the package:

```text
Photo 2 of 3.
When: 14 June 2026, from the file date, may be wrong.
Family says: the cake, lemon with blueberries.
AI guess: Three adults and a child stand around a round cake with candles.
Words in the photo, AI reading: HAPPY SUMMER.
```

Every line starts with its source, and family notes come before the AI guess. Names come only from the helper. The vision prompt forbids guessing identity, relationships, gender, age in years or feelings, and ID cards or medical scenes stay Not described. The helper reads the whole letter, adds notes by photo number and says save once, then confirms the platform approval if Uliya shows one. Later letters cover only new photos. When the listener asks something a photo cannot answer, the helper can keep the question for the family with one more approval, and the next letter carries the answer.

### How we built it

I built it alone, from Chile, without a NAS. The package is Markdown only: SKILL.md and six reference files, passing the official static checker with 0 diagnostics. It uses three experts: photo-agent (album, photo choice, vision-vlm, vision-ocr), file-agent (earlier letters, free file name, read-back) and knowledge-agent (save-text). A 6-photo letter takes 7 delegations. Claude Code helped me draft, review and script; I directed the work and edited the text.

To tune the prompts without the NAS model, I built a bench outside the package: 25 CC0, public-domain or synthetic images, plus 2 a reviewer added later, run on cloud stand-in models (Nemotron-3.5-Super-VL, MiMo-V2.6-Pro). No family photo went anywhere. A cloud model then played the Uliya parent agent against expert replies I wrote by hand.

### Challenges we ran into

- The first prompt answered Spanish requests in English 13 times out of 16. Naming the language on every line stopped that, though single English words still slip in.
- The prompt declined "which one is the groom?" in English, but not reliably in Spanish, German or Turkish. So the Skill answers person questions only from family notes, and they never reach the vision model.
- The dry run caught a save retried without approval. A fresh run of all eight scenarios then passed only 8 of 16 runs: family notes with a straight apostrophe broke the quoted command, answers to earlier questions fell outside the letter, and a denied save did not show the letter again. After two more rounds of fixes, 23 of 24 runs passed every critical check (419 of 421). The expert replies are hand-written and cooperative, so this is a smoke test, not proof.

### Accomplishments that we're proud of

- The listener hears where a line came from before the line itself.
- In every test, an ID card, a chat screenshot, a lab sheet and a hospital-bed photo were withheld, and no ordinary photo was wrongly withheld (small samples).
- The letter is saved once, never over an existing file, and read back before the Skill calls it saved.

### What we learned

Describing pixels is the easy part. A guess read aloud sounds as sure as a fact, so the label must come first. I also learned to distrust my numbers: the prompts were tuned on the images they were scored on, so these are development results, not validation.

### What's next for Album Out Loud

Honest status: nothing has run on a NAS, the NAS vision model is untested, and no blind or low-vision listener has heard a letter. If selected, I will run the quick test on the iDX6011 Pro and measure routing, time per photo, whether vision runs on the device, and how the save approval appears. Then blind and low-vision listeners on their own screen readers, and the open problems: Spanish gendered words, invented figures, labels in the listener's language.
