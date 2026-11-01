# Presentation assets: Album Out Loud

Assets for the Devpost page and the round 1 PDF. Nothing here goes into the Skill ZIP. The scripts that made them are in `submission/tools/`.

None of these assets comes from a NAS run. The Skill has not run on a NAS yet. No blind or low-vision person has heard or rated the letter.

## Assets

| File | What it is | How it was made |
|---|---|---|
| `flow_diagram.png` | The letter flow on 1600 x 2496 px: setup message, steps 1 to 8 in four lanes (chat, photo-agent, file-agent, knowledge-agent), and step 7 marked as the one approval of a letter. | `tools/make_images.py` (Pillow, Segoe UI). Steps, experts and approvals are taken from `app/album-out-loud/SKILL.md` and `references/capability-map.md`. |
| `sample_letter.txt` | A full English listening letter for 8 photos: a since letter with one family answer and one open question. | Hand-built by following `references/letter-format.md` line by line. The AI guess and Words lines are copied from tuning outputs (see the table below). Everything else is invented. UTF-8 without BOM, LF, typographic apostrophes only. |
| `sample_letter_es.txt` | The same letter for a Spanish-speaking listener. Labels and dates are in Spanish, and the For the helper part stays in English, as the format requires. | Same method. The AI guess lines are real Spanish outputs, not translations. |
| `sample_letter.wav` | The English letter read by the offline Windows voice Microsoft Zira Desktop: 4 min 13 s, 22,050 Hz, 16-bit mono. It stops after the closing line, where the letter tells the listener they can stop. | `tools/speak_letter.ps1` (PowerShell, System.Speech.Synthesis): a pause of 350 ms after each line and 900 ms at each empty line. No cloud service. It gives an idea of how a screen reader voice reads the letter. It is not a recording of NVDA, VoiceOver or TalkBack. |
| `letter_card.png` | Gallery image, 1600 x 1136 px: the opening lines and the first two entries of the English letter, with source labels in colour and the two photos shown for sighted readers. | `tools/make_images.py`. It reads the text from `sample_letter.txt`, so the card and the letter cannot drift apart. |
| `comparison.png` | A three-row table, 1600 x 808 px, comparing phone image describers, photo highlight and reminiscence tools (as generic categories) and Album Out Loud. | `tools/make_images.py`. The first two rows are general category summaries, not claims about any single product or entrant. |

Rebuild:

```text
uv run --with matplotlib --with pillow python -I submission/tools/make_images.py <project root>
powershell -NoProfile -ExecutionPolicy Bypass -File submission/tools/speak_letter.ps1
```

## What is real in the sample letters

Every AI guess and Words line was copied word for word from an output of Nemotron-3.5-Super-VL, a cloud stand-in model, saved during prompt tuning in `app/tuning/results/`. Only the Line 1 and Words labels were removed. Nothing in these lines was rewritten.

| Photo | File | English output (prompt variant, mode) | Spanish output (prompt variant, mode) |
|---|---|---|---|
| 1 | 11_bw_adult_baby.jpg | D, brief (`raw.jsonl`) | R2, rich, Line 1 only (`review_nemotron.jsonl`) |
| 2 | 12_cake_happy_birthday.jpg | B, brief (`raw.jsonl`) | B, brief (`raw.jsonl`) |
| 3 | 16_tshirt_portuguese.jpg | B, brief | B, brief |
| 4 | 08_beach_dog.jpg | E, brief | F, rich, Line 1 only (`review_nemotron.jsonl`) |
| 5 | 05_wedding_group.jpg | D, brief | F, rich, Line 1 only (`review_nemotron.jsonl`) |
| 6 | 25_dark_blurry_group.jpg | D, brief | B, brief |
| 7 | 22_synthetic_id_card.jpg | D, brief: Not described, ID card with personal data | B, brief: Not described, documento de identidad personal |
| 8 | 14_spanish_street_sign.jpg | B, brief | B, brief |

Limits of the sample:
- The lines come from several tuning rounds (B, D, E, F and the reviewer prompt R2). They do not come from one run of the final prompt in `references/vision-prompts.md`. In tuning, some photos only had a Spanish output from the rich prompt, so its Line 1 is used in place of a brief answer.
- vision-ocr was never run, so no Words line can be confirmed. Every Words line therefore carries the label Words in the photo, AI reading, as the format requires.
- Invented: the album name, the listener (Dad), the helper (Ana), every family note and name, dates, times, places, the earlier letter, its question and its answer, and the file paths. Paths are shortened, as in the example in `letter-format.md`, and use the tuning file names so each entry can be traced to its image.
- The Spanish letter says 6:40 and 7:52 de la tarde and 8:15 and 11:48 de la noche, which is how people in Chile say these times. The letter format leaves this to the listener language.
- The photos show strangers from public collections. They stand in for a family album and do not show a real family.

## Image credits

All photos are from Wikimedia Commons or were made for the tuning bench. Licences and sources are as recorded in `app/tuning/manifest.csv`.

| File | Author | Licence | Source |
|---|---|---|---|
| 11_bw_adult_baby.jpg | Willem van de Poll | CC0 | https://commons.wikimedia.org/wiki/File:Gudrun_L%C3%A1rusd%C3%B3ttir_met_haar_oudste_kleinkind_op_de_arm,_Bestanddeelnr_252-1777.jpg |
| 12_cake_happy_birthday.jpg | Brassluff | CC0 | https://commons.wikimedia.org/wiki/File:Price_of_Cake_with_a_Baked_Shape_of_Happy_Birthday.jpg |
| 16_tshirt_portuguese.jpg | Eugenio Hansen, OFS | CC0 | https://commons.wikimedia.org/wiki/File:Brazil_-_Software_patent_-_No_-_T-shirt.JPG |
| 08_beach_dog.jpg | Alvin Balemesa (alnbal) | CC0 | https://commons.wikimedia.org/wiki/File:Family_at_Cottesloe_beach_(Unsplash).jpg |
| 05_wedding_group.jpg | Seven心視界 | CC0 | https://commons.wikimedia.org/wiki/File:2021-09-17_wedding_guests_with_groom_in_Tuku,_Yunlin.jpg |
| 25_dark_blurry_group.jpg | Tuning bench, darkened and blurred from a CC0 photo | CC0 (derivative of CC0) | https://commons.wikimedia.org/wiki/File:Bari_Adult_Literacy_Graduation_Ceremony_%E2%80%94_Bidibidi_Refugee_Settlement,_Uganda_2026.jpg |
| 22_synthetic_id_card.jpg | Tuning bench (`app/tuning/make_synthetic.py`), fake data | CC0 (own work) | synthetic |
| 14_spanish_street_sign.jpg | Alavense | CC0 | https://commons.wikimedia.org/wiki/File:Calle_de_Escoriaza,_Vitoria_(2).jpg |

`letter_card.png` shows photos 11 and 12 only. `flow_diagram.png` and `comparison.png` use no photos. Fonts are Segoe UI, which ships with Windows, and only the rendered images are shared.
