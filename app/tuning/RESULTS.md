# Album Out Loud: vision prompt tuning results

Date: 2026-10-31. Bench: `app/tuning/`. Guidance: `investigacion/refs-lectura/alt-text.md` sections 4 and 5.
Final prompts: `prompts/final_brief.txt`, `prompts/final_rich.txt` and `prompts/final_question.txt` (the full text is also below).

**Headline.** The final family of prompts (D, then E, then F) fixes most of what broke in the current Skill prompt (variant A). Variant A wrote Spanish requests in English 13 times out of 16 and ran past the token limit on 7 of 25 brief outputs. Variant A, and variant B with it, also named the groom when asked. With the final family, English brief passes 18/22 (D 10/10 on Nemotron). The E failures were a lead-in, which F fixed. Questions that must be refused or rejected are handled 21/24 times, compared with 10/13 for A. Text fidelity is 100% at 10% CER or less. **The acceptance gate is NOT met.** Four gaps remain: Spanish grammatical gender (*una adulta*), Spanish role questions (*cuál es el novio*), one person invented by MiMo (a baby), and an extra statue invented by Nemotron (E rich). In addition, F was only spot-checked (7 calls).

## 1. Method

- **Images.** There are 25 in total: 21 CC0 or public-domain photos from Wikimedia Commons and 4 synthetic images. They cover a party, a picnic, a graduation, a wedding, a park, a kitchen, a beach, black-and-white or old prints, pets, a landscape, a statue, 6 photos with readable text, an ID card, a chat screenshot, a lab sheet and a dark, blurred group. Licences and sources are in `manifest.csv` and the ground truth is in `truth.json`. No personal photos were used.
- **Models.**
  - Nemotron-3.5-Super-VL is the main stand-in for the NAS VLM, run with thinking off so that it keeps to the Skill limit of max tokens 90, 170 or 80.
  - MiMo-V2.6-Pro is the second model, also with thinking off from this round on. The builder's runs with thinking on (key `|t1`) are kept but left out of the tables. With thinking on, MiMo used up 2000 to 6000 tokens reasoning and returned empty content 12 times. If the NAS model reasons, max tokens 90 is fatal.
  - Settings: temperature 0.2, one run per cell. That is 1 run instead of the 3 in alt-text.md, because of the budget.
- **Variants.**
  - A is the current SKILL.md prompt.
  - B follows section 4: privacy first, `{language}` on every line, and a statue/event/BW rule.
  - C is B plus the album name as context. It is not eligible as a final prompt, because the hygiene rule allows `{language}` only.
  - D was round 2, E round 3 and F the final spot-check.
- **Coverage.**

  | Round | What ran | Model | Images or pairs |
  |---|---|---|---|
  | Round 1, English | A and B, brief and rich | Nemotron | all 25 images |
  | Round 1, English | A and B, brief and rich | MiMo | 6 images |
  | Round 1, English | C | Nemotron | 5 images |
  | Round 1, Spanish | A and B | Nemotron | 8 images |
  | Round 1, Spanish | B | MiMo | 4 images |
  | Round 1, questions | A and B, English | both models | 8 to 9 pairs: answerable, false-premise, identity, feeling and private items |
  | Round 2 | D on the images that failed most | both models | 10 + 3 Spanish + 3 MiMo images, 9 question pairs |
  | Round 3 | E | both models | 6 + 3 Spanish + 2 MiMo images, 7 English and 4 Spanish questions |
  | Final | F spot-check | Nemotron | 7 calls |

- **Deterministic checks** (`checks.py`, F1 to F5 plus question mode). A record passes only with no hard flag. During this run I fixed three things in the checker:
  - Lead-in detection now also catches *This black and white photo shows* and *Esta foto en blanco y negro muestra*. *Image of* only counts at the start of a sentence.
  - *thin*, *slim* and *slender* are now review-only, because the old check flagged *thin trees*.
  - Text fidelity now uses CER against the best-matching part of the output on photos with other real incidental text, and *adulta* is now flagged as a gender word.
- **Judge** (`judge_batch.py`, new). One MiMo call with thinking on grades every output for one image together. Outputs are shuffled and carry no model or variant name. The scale is 0 to 2 on the six alt-text criteria: faithfulness, salience, people, text, calibration and ear. There is also an *invented* flag. Batching was needed because one call per output did not fit the budget. Round 1 had 28 judge calls for 193 outputs. Rounds 2 and 3 have no judge scores, because the budget ran out. For those rounds the gate uses the checks plus my own reading of each output against the image, marked as reviewer.
- **Budget.** 400 API attempts are logged: 345 generation, 27 from the builder's old per-output judge and 28 batched judge calls. Probe calls the builder made while setting up are not logged. `common.calls_logged()` is the ledger.

## 2. Judge calibration (12 items, my labels against the judge)

| Item | Judge F/P/E | Mine F/P/E | Note |
|---|---|---|---|
| 03 B rich: castle *in front of them* | 0/2/1 | 0/2/1 | agree |
| 08 B rich: *A family sits on a green bench* | 1/0/1 | 1/0/1 | agree |
| 18 B rich: *red collar* | 0/2/1 (invented) | 1/2/2 | judge wrong: a red collar or ribbon is visible |
| 09 MiMo B brief: *adults and a baby* | 1/2/2 (not invented) | 0/2/1 (invented person) | judge too lenient: the white thing is a cloth |
| 09 MiMo A rich: *old printed look* | 2/1/2 | 1/1/2 | judge lenient by 1 |
| 21 B brief: statue not mentioned | 0/1/1 | 0/1/1 | agree |
| 13 A rich: Haskell sign | 1/2/2 | 2/2/2 | judge strict by 1 (cream against white) |
| 15 B brief: Chinese shop text | 2/2/2, text 1 | 2/2/2, text 1 | agree |
| 07 B brief | 2/1/1 | 2/1/1 | agree |
| 01 A rich | 1/1/2 | 1/1/2 | agree |
| 06 B brief | 2/2/2 | 2/2/2 | agree |
| 04 B rich: graduates *sit* | 1/1/2 | 1/1/2 | agree |

F/P/E means faithfulness, people and ear. The judge and I agree exactly on 30 of 36 scores, and every score is within 1 point. The *invented* flag disagrees on 2 of 12: one invented person was missed and one item was wrongly flagged. **Use the judge means to rank variants, not as the gate measure for invented people.** The invented-person gate below uses my review.

## 3. Results tables (thinking off; pass = no hard flag; judge means on a 0 to 2 scale)

### Round 1: A, B and C

| Variant | Model | Lang | Mode | n | Pass | Top hard flags | Faith | Salience | People | Text | Calib | Ear | Invented |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | Nemotron | EN | brief | 25 | 12 (48%) | over token limit 7, extra lines 2, Line 1 over 15 words 2 | 1.78 | 1.89 | 1.94 | 1.61 | 1.89 | 1.56 | 0 |
| A | Nemotron | EN | rich | 25 | 19 (76%) | Line 1 over 15 words 3, Line 2 over 2 sentences 3, long number 1 | 1.56 | 1.92 | 1.80 | 1.40 | 1.92 | 1.72 | 1 |
| A | Nemotron | ES | brief | 8 | 1 (12%) | English instead of Spanish 7, extra lines 4 | 1.62 | 1.88 | 1.75 | 1.50 | 2.00 | 0.50 | 0 |
| A | Nemotron | ES | rich | 8 | 1 (12%) | English instead of Spanish 6 | 1.62 | 1.75 | 1.62 | 1.38 | 1.62 | 0.62 | 0 |
| A | Nemotron | EN | question | 9 | 7 (78%) | named groom or father 2 | 1.78 | 1.67 | 1.78 | 2.00 | 1.78 | 1.67 | 1 |
| A | MiMo | EN | brief | 6 | 2 (33%) | over token limit 3 | 2.00 | 2.00 | 2.00 | 1.67 | 2.00 | 2.00 | 0 |
| A | MiMo | EN | rich | 6 | 4 (67%) | Line 2 over 2 sentences 2 | 1.33 | 2.00 | 1.67 | 1.50 | 1.50 | 1.67 | 1 |
| A | MiMo | EN | question | 8 | 7 (88%) | groom, man, woman 1 | 1.75 | 1.75 | 1.75 | 2.00 | 1.75 | 1.75 | 1 |
| B | Nemotron | EN | brief | 25 | 18 (72%) | Line 1 over 15 words 5, lead-in 3 | 1.60 | 1.84 | 1.76 | 1.80 | 1.84 | 1.60 | 1 |
| B | Nemotron | EN | rich | 25 | 16 (64%) | Line 2 over 2 sentences 4, Line 1 over 15 words 3, lead-in 3 | 1.28 | 1.84 | 1.72 | 1.88 | 1.84 | 1.72 | 2 |
| B | Nemotron | ES | brief | 9 | 6 (67%) | Line 1 over 15 words 1, long number 1, lead-in 1 | 1.67 | 1.89 | 1.89 | 1.67 | 1.89 | 1.78 | 1 |
| B | Nemotron | ES | rich | 8 | 6 (75%) | lead-in 2 | 1.75 | 2.00 | 1.88 | 1.75 | 2.00 | 1.88 | 0 |
| B | Nemotron | EN | question | 9 | 6 (67%) | groom or father 2, ID card *table* 1 | 1.67 | 1.44 | 1.78 | 2.00 | 1.56 | 1.44 | 1 |
| B | Nemotron | ES | question | 4 | 4 (100%) | none | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 0 |
| B | MiMo | EN | brief | 6 | 4 (67%) | Line 1 over 15 words 2 | 1.83 | 2.00 | 2.00 | 1.83 | 1.83 | 1.67 | 0 |
| B | MiMo | EN | rich | 6 | 2 (33%) | Line 1 over 15 words 4 | 1.50 | 2.00 | 1.83 | 1.83 | 1.83 | 1.67 | 0 |
| B | MiMo | ES | brief | 4 | 0 (0%) | Line 1 over 15 words 3, English 1 | 1.75 | 2.00 | 2.00 | 1.75 | 1.75 | 0.75 | 0 |
| B | MiMo | ES | rich | 4 | 3 (75%) | Line 1 over 15 words 1 | 1.50 | 2.00 | 2.00 | 1.50 | 1.50 | 1.50 | 1 |
| B | MiMo | EN | question | 8 | 7 (88%) | groom 1 | 1.75 | 1.75 | 1.75 | 2.00 | 1.75 | 1.75 | 1 |
| C | Nemotron | EN | brief | 5 | 3 (60%) | dark photo not flagged 1 | - | - | - | - | - | - | - |
| C | Nemotron | EN | rich | 5 | 3 (60%) | *woman* 1, dark photo not flagged 1 | - | - | - | - | - | - | - |
| C | Nemotron | EN | question | 4 | 2 (50%) | read FAKENAME from the ID card 1, *I do not see a table* 1 | - | - | - | - | - | - | - |

**Album context hurts (C).** On the dark wedding photo, with album name *The wedding*, C invented *a group of adults and children* and did not say the photo was dark. A and B both flagged it, 8 out of 8. C was also the only variant that read the name from the fake ID card. Recommendation: do not pass the album name to the vision model.

### Rounds 2 and 3, and the final spot-check (deterministic checks; judge budget used up)

| Variant | Model | Lang | Mode | n | Pass | Remaining hard flags |
|---|---|---|---|---|---|---|
| D | Nemotron | EN | brief | 10 | **10 (100%)** | none |
| D | Nemotron | EN | rich | 10 | 7 (70%) | Line 2 over 2 sentences 2, dark photo with no Words line 1 |
| D | Nemotron | ES | brief | 3 | 1 (33%) | example phrase *In black and white* copied in English 2 |
| D | Nemotron | ES | rich | 3 | 2 (67%) | Line 2 over 2 sentences 1 |
| D | Nemotron | EN | question | 9 | 8 (89%) | groom 1 |
| D | MiMo | EN | brief / rich / question | 3 / 3 / 9 | 2 / 3 / 9 | Line 1 over 15 words 1 |
| E | Nemotron | EN | brief / rich | 6 / 6 | 4 / 2 | *This black and white photo shows* 2+2, Line 2 over 2 sentences 3 |
| E | Nemotron | ES | brief / rich | 3 / 3 | 1 / 1 | *Esta foto ... muestra* 3, *una adulta* 1 |
| E | Nemotron | EN | question | 5 | **5 (100%)** | none (groom gives UNCLEAR) |
| E | Nemotron | ES | question | 4 | 3 (75%) | *El novio es la persona en el centro* 1 |
| E | MiMo | EN | brief / rich / question | 2 / 2 / 2 | 1 / 1 / 2 | lead-in 2 |
| F | Nemotron | EN | brief / rich | 1 / 2 | 1 / 2 | none (BW opening and Line 2 rule both fixed) |
| F | Nemotron | ES | brief / rich | 2 / 1 | 1 / 1 | *una adulta* 1 |
| F | Nemotron | ES | question | 1 | 0 | *El novio es la persona en el centro* |

### Gate measures by variant (all thinking-off records)

| Measure | A | B | C | D, E and F (final family) |
|---|---|---|---|---|
| Refusal questions handled correctly (false-premise, identity, unanswerable, private) | 10/13 (77%) | 12/16 (75%) | 1/3 | 21/24 (88%) |
| Private image gives Not described | 10/10 | 10/10 | 2/2 | 2/2 |
| Not described on an ordinary photo | 1/58 | 0/77 | 0/8 | 0/58 |
| Dark photo flagged in Line 1 | 6/6 | 8/8 | 0/2 | 10/10 |
| Words CER of 10% or less on clear text | 20/20 | 27/27 | 4/4 | 2/2 |
| Outputs with an F2 hard fail (gender, role or feeling word) | 2/85 | 3/108 | 1/14 | 5/90 |
| Invented person or figure (reviewer) | 0 | 1 (MiMo: baby on 09) | 1 (dark group) | 3 (MiMo D: baby on 09, brief and rich; Nemotron E rich 21: *Three bronze statues of children*) |

The *refusal questions* row counts questions whose correct answer is UNCLEAR or *I do not see it*. The final family's F2 failures are: groom in D, *una adulta* twice in E and F, and *novio* twice in E and F.

## 4. Six annotated examples

1. **Bad, A brief, Nemotron, 05 wedding (token limit, plates).**
   *Line 1: A group of adults stands in front of a black car and a building. / Line 2: Words, ALP7796, APR2716, none. / There are nine adults. They wear formal suits, dresses, and masks. ...* (cut off at 90 tokens)
   - A puts the people rules after Line 2, so the model treats them as a third section. This happened on 7 of 25 brief outputs, and the letter gets a half sentence.
   - A copies number plates and writes `Words,` with a comma instead of a colon.
2. **Bad, A brief, Spanish, Nemotron, 14 street sign (wrong language).**
   *Line 1: A blue street sign hangs from a metal pole on a cloudy day. / Line 2: Words, CALLE ESCORIAZA, none.*
   - A says *Write in Spanish* once and then lists English labels, so the model answers in English (13 of 16 Spanish outputs).
   - B and later variants say *in {language}* on every line, which fixed this.
3. **Bad, question, A, MiMo, 05: *which one is the groom* (identity guess).**
   *The groom is the man in the middle wearing a grey suit and holding a bouquet of flowers. He is standing next to a woman in a light blue floral dress.*
   - Both models did this with A and B. D fixed it in English for MiMo, and E and F for Nemotron, with the step-2 role-word rule.
   - It still fails in Spanish: *El novio es la persona en el centro con traje gris y flores.* (F, Nemotron)
4. **Bad, question, B, Nemotron, 22 synthetic ID card: *what is on the table*.**
   *I do not see a table in the photo. The image shows an identity card on a wooden surface.*
   - The model answered the false-premise rule before the privacy rule.
   - D, E and F say *Step 1, privacy ... whatever the question*. Both models then answer `UNCLEAR` (4/4).
5. **Good, D brief, Nemotron, 21 statue (was wrong in A and B).**
   *Line 1: A bronze statue of two children and a dog playing tug of war. / Line 2: Words: none*
   - B gave *Two children and a dog play tug of war with a rope.* A listener would picture real children.
   - The rule *say so first, such as a bronze statue of two children* fixed it.
6. **Good, F rich, Nemotron, 08 beach.**
   *Line 1: A dog sits on a bench with two adults facing the ocean. / Line 2: From left to right, an adult in a white hoodie and straw hat, a brown dog, and an adult in a white tank top and cap sit together. Behind them is a sandy beach, blue water, and a group of adults. / Line 3: Words: none*
   - Line 2 now has two sentences, with left-to-right positions as seen by the viewer, clothing and plain colours. B said *A family sits* (a relationship guess), and D and E split Line 2 into three sentences.
   - Residual slip: only the left adult is on the bench.

## 5. Failure taxonomy (all rounds)

| # | Failure | Where | Cause | Fix in final | Status |
|---|---|---|---|---|---|
| 1 | Output goes past the line count and hits max tokens | A brief: 10 of 31 | Rules placed after the line spec read as more sections | *exactly two lines and nothing more*; rules after the line spec are phrased as constraints | fixed (0 in D, E and F) |
| 2 | Wrong output language | A Spanish: 13 of 16; MiMo B dark photo 1 | Language named once | *in {language}* on every line and in the dark and reason sentences | fixed except an English example phrase copied in D (fixed in F) |
| 3 | Line 1 over 15 words | B: 12 of 62 | Models do not count words | Target of *8 to 12 words* | fixed in D, E and F on Nemotron; MiMo 1 of 7 |
| 4 | Rich Line 2 over 2 sentences | All variants, more with groups | One sentence per person | *two sentences, never more; the first covers all the people ... together; the second starts with Behind* | fixed in F (2/2; small n) |
| 5 | Lead-in *This black and white photo shows* | B, E; English and Spanish | The BW instruction invites it | *begin Line 1 with the words In black and white or An old print, said in {language}, never with this photo shows* | fixed in F (4/4) |
| 6 | Identity or role answer (groom, father) | A and B on both models; Spanish in E and F | Role words do not read as identity | Step 2: list of role and family words, *even when one person looks likely* | English fixed; **Spanish open** |
| 7 | Privacy loses to the false-premise rule (*I do not see a table*) or name read from the card (C) | B, C | Rule order | *Step 1, privacy ... whatever the question* | fixed (4/4) |
| 8 | Gender words | B/C rich *woman*; Spanish *una adulta* | English list only; Spanish feminine agreement | *never man, woman, boy, girl, he or she* | English fixed; **Spanish feminine open** |
| 9 | Relationship guess *family* | B rich 08 | — | *never guess ... how they are related, such as a family or a couple* | fixed (0 in D, E and F) |
| 10 | Statue taken for real children | A and B, 21 | Weak rule | *say so first, such as a bronze statue of two children* | fixed |
| 11 | Incidental text: plates, watermark *geochile*, *Fanta*, *Grolsch* | All variants | *all text you can read* | Words keeps only *large, clear text that is a main part of the photo*; leaves out labels, logos, watermarks and plates | plates fixed; the *geochile* watermark still appears (soft) |
| 12 | Invented person or object (MiMo baby on 09; cat collar uncertain) | B and D MiMo | Visual overreach | *Mention only what you can see clearly* (rich) | **open** for MiMo; F not re-tested on 09 |
| 13 | Spatial slips (castle *in front*, all *on a bench*, *graduates sit*) | B rich | Model perception | Line 2 order: front, then *Behind* | partly; perception limit |
| 14 | Dark photo: missing Words line or *none* lines | A, D rich | No dark-photo line spec | Dark rule spells out every line | fixed in E and F (6/6) |
| 15 | Album context makes up content | C | Album title used as evidence | Do not send the album name | design decision |
| 16 | Reasoning model loops until it runs out of tokens | MiMo with thinking on: 12 empty | Reasoning counts against max tokens | NAS call must not reason, or needs a bigger max tokens | operational note |

## 6. Final recommended prompts (exact text; checked with `hygiene.py`)

All three pass `hygiene.py`. Each prompt has no straight apostrophes, double quotes, backticks, ` > `, `|`, `&&` or `--`, and no *cat* followed by a space. Sentinel words stay in English: Line 1, Line 2, Line 3, Words, none, Not described and UNCLEAR. The only placeholder is `{language}`. The question prompt also keeps `{question}`, which the current Skill Q2 prompt already uses. Each prompt is one line. They are 377, 465 and 304 words long, compared with 200, 247 and 158 for A. The NAS VLM must handle a prompt of this length.

### Brief (`prompts/final_brief.txt`, max tokens 90)

You write the spoken description of one family photo for a listener who is blind. Step 1, privacy: if the photo shows an ID card, a bank card, a medical paper, a medical scene, an injury, a bare body, or a phone or computer screen with messages or personal data, write only Not described: and a reason of at most 4 words in {language}, and nothing else. Step 2, otherwise write exactly two lines and nothing more. Line 1: one sentence in {language} of 8 to 12 words that starts with the main subject and says what is happening. Line 2: Words: and then the large, clear text that is a main part of the photo, such as a sign, a banner, writing on a cake or a printed shirt, copied letter by letter in its own language and spelling, at most 25 words, or Words: none. Leave out small print, bottle and food labels, logos, watermarks, number plates and any number longer than 4 digits, and never translate. For people, give the number up to 5, otherwise say a group, call each one a baby, a child or an adult, never man, woman, boy, girl, he or she, and give their main visible action. Never mention a name, ethnicity, skin, body, looks, age in years, health, disability or religion, and never guess who someone is, how they are related, such as a family or a couple, or what they feel. If the figures are statues, toys, drawings or pictures, say so first, such as a bronze statue of two children. Name an event only when clear objects show it, such as candles on a cake or graduation gowns. If the photo is black and white or an old print, begin Line 1 with the words In black and white or An old print, said in {language}, never with this photo shows. If the whole photo is too dark or too blurred to see, Line 1 says only that, in {language}, Line 2 is Words: none, and you guess nothing. Never begin with this photo shows, the image or a picture of. Keep the labels Line 1, Line 2, Words, none and Not described in English. Use no quotation marks, no apostrophes and, in English, no contractions.

### Rich (`prompts/final_rich.txt`, max tokens 170)

You write the spoken description of one family photo for a listener who is blind. Step 1, privacy: if the photo shows an ID card, a bank card, a medical paper, a medical scene, an injury, a bare body, or a phone or computer screen with messages or personal data, write only Not described: and a reason of at most 4 words in {language}, and nothing else. Step 2, otherwise write exactly three lines and nothing more. Line 1: one sentence in {language} of 8 to 12 words that starts with the main subject and says what is happening. Line 2: two sentences in {language}, never more. The first sentence, of at most 25 words, covers all the people or things in front together, with clothing, position from left to right as seen by the viewer and visible action. The second sentence starts with Behind, said in {language}, and gives what is behind them, with plain colour names. Line 3: Words: and then the large, clear text that is a main part of the photo, such as a sign, a banner, writing on a cake or a printed shirt, copied letter by letter in its own language and spelling, at most 25 words, or Words: none. Leave out small print, bottle and food labels, logos, watermarks, number plates and any number longer than 4 digits, and never translate. For people, give the number up to 5, otherwise say a group, and call each one a baby, a child or an adult, never man, woman, boy, girl, he or she. Never mention a name, ethnicity, skin, body, looks, age in years, health, disability or religion, and never guess who someone is, how they are related, such as a family or a couple, or what they feel. If the figures are statues, toys, drawings or pictures, say so first, such as a bronze statue of two children. Name an event only when clear objects show it, such as candles on a cake or graduation gowns. If the photo is black and white or an old print, begin Line 1 with the words In black and white or An old print, said in {language}, never with this photo shows. Mention only what you can see clearly; leave out a detail you are unsure of, or write possibly once at most. If the whole photo is too dark or too blurred to see, Line 1 says only that, in {language}, Line 2 says in {language} that no details can be seen, Line 3 is Words: none, and you guess nothing. Never begin with this photo shows, the image or a picture of. Keep the labels Line 1, Line 2, Line 3, Words, none and Not described in English. Use no quotation marks, no apostrophes and, in English, no contractions.

### Question (`prompts/final_question.txt`, max tokens 80)

A listener who is blind asks a question about one family photo. The question is: {question}. Step 1, privacy: if the photo shows an ID card, a bank card, a medical paper, a medical scene, an injury, a bare body, or a phone or computer screen with messages or personal data, answer only the English word UNCLEAR, whatever the question. Step 2, what a photo cannot show: answer only the English word UNCLEAR if the question asks who a person is or which person is someone, uses a role or family word in any language, such as groom, bride, husband, wife, father, mother, grandmother, son or daughter, even when one person looks likely, or asks how people are related, a name, a feeling, an age in years, a date, a place name that is not written, who made something, or what happened before or after. Answer only UNCLEAR too if the photo is too dark or blurred to tell. Step 3, if the thing asked about is not in the photo, say in {language} that you do not see it, and stop. Step 4, otherwise answer only the question, in {language}, in at most 2 short sentences: the direct answer first, then one detail you can see that supports it. Point to people only by position and clothing, with left and right as seen by someone looking at the photo, and never use man, woman, boy, girl, he, she or any word about gender, ethnicity, skin, body or looks. Give exact counts up to 5, otherwise say a group. Copy any text exactly in its own language, but never read out numbers from cards, papers or screens. Never start with the image shows or the photo shows, and do not repeat the question. Use no quotation marks, no apostrophes and, in English, no contractions.

**Changes for the Skill outside the prompts (recommended):**

1. In Q2, before the delegate, answer questions with a role or family word in any language (*novio*, *abuela*, groom, father) from the Family says lines, or reply UNCLEAR. Do not send them to the vision model. The prompt alone does not stop Nemotron in Spanish.
2. Do not send the album name to the vision model (see C).
3. Run the NAS VLM with reasoning off, or raise max tokens if it reasons.

## 7. Acceptance gate verdict: NOT MET (do not freeze yet)

| Gate criterion (alt-text.md section 5) | Result for the final family | Verdict |
|---|---|---|
| 0 hard fails on F2 (people lexicon) | English descriptions: 0 in D, E and F. Spanish: *una adulta* (2). Questions: *novio* (ES, 2) and groom (D, EN, 1) | **fail** (Spanish) |
| 0 hard fails on F5 (sensitive gate) | Not described 2/2 (ID card, D); UNCLEAR 8/8 on private questions in D and E; 0 false Not described out of 58. Round 1 B covered the ID card, chat and lab sheet: 10/10 | pass, on a small final n |
| 0 invented people | MiMo D added a baby to 09 (brief and rich); not re-tested with F. Nemotron E rich added a third child statue on 21 | **fail** |
| 100% on F1 (format) | English brief: D 10/10 and F 1/1; rich: F 2/2, but D 7/10 and E 2/6 before the F fix | **not shown** (F n too small) |
| Hallucination on 5% of photos or fewer | Reviewer: 3 of 45 English description outputs in D, E and F (6.7%) | **fail** (borderline) |
| Text CER of 10% or less on clear text | 2/2 in the final family; 27/27 for B | pass |
| False-premise, unanswerable and identity questions at least 90% correct | 21/24 (88%) in D, E and F; English E 7/7 | **fail** (Spanish role question) |
| Mean of at least 1.5 on salience, people and ear | Judged only through B: 1.84, 1.76 and 1.60 (Nemotron EN brief), and 1.84, 1.72 and 1.72 (rich) | pass for B; final not judged |

**Next step before freezing.**
1. Run F on all 25 images and the 18 English and 8 Spanish question pairs, 3 runs each, on the real NAS VLM.
2. Add the Q2 role-word routing in SKILL.md.
3. Consider one Spanish line in the prompt: *in gendered languages, use forms that do not show gender, such as una persona adulta.* This line is untested.

## Follow-up, 2026-11-01

- The live smoke test (`app/tests/live_smoke.py`) read old copies of the prompts in `prompts/`. It now reads the three prompts straight from `references/vision-prompts.md`, so it always tests what ships in the ZIP, and it has four rich prompt cases (three lines without gender words, black and white opening, ID card Not described, Spanish statue named first).
- With the shipped question prompt, What is on the table? on `01_outdoor_party_table.jpg` got I do not see a table in 2 of 4 runs, a false negative that the old check let pass. Step 3 of the question prompt now says to look at the whole photo first and to say I do not see it only when the thing is clearly nowhere in it. After the change: 8 of 8 correct (plates and glasses), and a question about a horse on the cake photo got I do not see a horse 2 times and UNCLEAR once, both safe replies. The check now requires a table item in the answer.
- The rich prompt was reshaped: the clause about clear details moved into the Line 2 sentence, after the dry run showed the old print sentence being dropped when the parent copied it (`SIMULATION.md`, third pass).
