# Album Out Loud: dry-run simulation of the parent agent

Date: 2026-10-31. Harness: `app/tuning/simulate.py`. Raw transcripts: `app/tuning/results/sim/S*_r*.json`, summary in `results/sim/summary.json`.

## What this is, and what it is not

- A cloud model (`primalabs-ai/Nemotron-3.5-Super-VL-NVFP4`, thinking off, temperature 0.2) played the Uliya parent agent. Its system prompt was a 7-line harness preamble, then SKILL.md, then all six reference files that SKILL.md links (52,435 characters in total).
- The harness played the user and every expert. Each expert result is a mock I wrote: album lists, search-picture items with paths and capture times, meta places, vision outputs copied from the tuning runs (`results/raw.jsonl`), save-text `outputFile`, `contentBytes` and `verified=true`, `waiting_approval`, `cancelled`, `no results` and `failed`.
- Nothing ran on a NAS. The Uliya parent model, the real experts and the NAS vision model were not tested. Nemotron is a stand-in, and how the real parent behaves can differ. The mocks are cooperative: they return what each instruction asks for, so this tests whether the parent follows the Skill, not how the experts behave.
- Every delegate the model emitted was parsed and checked: the target is one of the 6 registered agents, the instruction is single-quoted with no straight apostrophe inside, there are no double quotes, backticks, two hyphens, `>`, `<`, `|`, `$(` or `&&`, no `{slot}` is left, there is no line break outside steps 7 and Q3, no value is copied from the synthetic examples, and every path, UUID and time appears in an earlier mocked result or user turn.
- API calls: at most 114 of the 120 allowed. That is 90 in the 16 kept runs, 16 in the two discarded first S1 runs, 3 in a trial S5 run that is not counted below, and up to 5 in an S7 run lost to a harness crash.
- The two S1 runs are partial replays. The first batch had a harness bug: the mock read the listener language from the words `in Spanish`, which appear in every brief prompt, so English photos got Spanish answers. In the kept S1 runs, the first 6 recorded model turns (two setup messages, steps 1, 3, 4a and 4b) are fed back unchanged, the mocks run again with the bug fixed, and the model runs live from the preview onward. Those 6 turns do not depend on the vision text, so the replay changes no model decision. S4 run 1 went through the same bug, but its photos had no Spanish mock entries, so it received the correct English answers.
- Two runs per scenario at temperature 0.2 is a smoke test. A defect seen 2 times out of 2 is likely to come back; one seen once out of 2 may be rarer.

## Results per scenario

Critical checks passed per run (minor checks are listed under the defects).

| Scenario | Run 1 | Run 2 | Delegate path seen | Verdict |
|---|---|---|---|---|
| S1 first letter, 8 photos | 48/52 | 48/53 | 1, 3, 4a, 4b, 6, 7, 8 (run 2 repeated 6 and 7) | FAIL 2/2 |
| S2 album not found | 7/7 | 7/7 | 1 | PASS 2/2 |
| S3 several albums match | 8/8 | 8/8 | 1, then 3 after the pick | PASS 2/2 |
| S4 since the last letter, 2 new photos, family answer | 22/28 | 25/28 | 1, 2, 3, 4, 6, 7, 8 | FAIL 2/2 |
| S5 relayed visible question, photo 4 | 11/14 | 11/14 | Q1, Q2 | FAIL 2/2 |
| S6 relayed identity question | 11/13 | 9/13 | Q1, Q3 (run 2: Q1, Q2, Q3) | FAIL 2/2 |
| S7 waiting_approval, then denied | 14/16 | 14/16 | 1, 3, 4, 6, 7 | FAIL 2/2 (apostrophe only) |
| S8 Spanish listener, up to the preview | 21/21 | 21/21 | 1, 3, 4 | PASS 2/2, 3 minor defects |

What held up in every run:
- No delegate went to an unregistered target, no `{slot}` was left, there was one command per message, and no expert result was invented. The step 1, 2, 3, Q1 and Q2 instructions were copied word for word from SKILL.md.
- The brief and rich vision prompts were copied exactly, with max tokens 90 or 170 and the right group sizes (P1 to P4, P5 to P8). The only prompt mismatch was the language (D3).
- In since mode, step 3 got the previous Newest photo checked time and all 8 earlier paths as already listed (2/2).
- No AI guess line held a name or a gender word, and no letter held a weekday. Selection rule: 1, Newest photo checked and the Photo N: lines came out right, the photo files section was last, the ID card stayed Not described, the file-date photo said from the file date, may be wrong, and Family says came before AI guess.
- S2 stopped after no results and offered the suggestions without searching further. S3 listed the three albums, waited for the pick, and sent step 3 with the right UUID and photo count of 22.
- S7: during waiting_approval the model claimed no save and sent no new command. After the denial it said nothing was saved, showed the full letter again and did not retry (2/2).

## Transcript excerpts

S2, after `no results` (both runs):
> No album or folder named Beach week 2025 was found. The closest matches are Beach week 2024 and Beach day. Would you like me to use one of those, or tell me the exact album or photo folder name?

S5, the Q2 vision call in both runs (Family says for photo 4: Grandpa’s dog Toby, with Grandpa on the left and Aunt Rosa on the right):
> ... Prompt begins: A listener who is blind asks a question about one family photo. The question is: what is Grandpa wearing?. Step 1, privacy: ...

S6 run 1, then the user says `yes, keep it for the family`, and the next model message is the Q3 save command, with no `save now` step in between:
> In Listening letter - Grandpa's 80th birthday - 2026-09-12 18-40.txt, photo 7.
> The entry has no Family says line, so this is a person question the notes do not answer. The photo cannot tell us that. Shall I keep the question for the family?

S1 run 1, final report:
> Saved and checked: /volume1/homes/ana/Listening letter - Grandpa's 80th birthday - 2026-09-12 18-40, a dash and the first free number from 2, .txt, 2813 bytes, 8 photos, 1 not described.

S1 run 2, step 7 returned `failed: the name exists`. With no new `save` from the helper, the model re-sent step 6 and then step 7 under the name `... 18-40, dash 2.txt`.

S4 run 1, the user types `A1: Aunt Rosa is holding baby Tomás, her grandson.`, and the next model message is the step 6 command. The letter with the answer was never shown and the user never said save.

S7 run 1, after waiting_approval:
> The platform is waiting for your approval to save the letter.
> File: Listening letter - Toby at the beach - 2026-08-03 10-12.txt
> Location: /volume1/homes/ana
> Please approve or deny in the dialog. Nothing is saved yet.

S8, a letter for a Spanish listener (both runs):
> Photo 2 of 4.
> When: 20 July 2026, 13:42.
> Where: Valparaíso.
> AI guess: Un trozo de pastel de chocolate con una decoración blanca sobre un plato blanco con borde amarillo.
> Words in the photo: Happy Birthday (AI reading).

## Skill defects found (most severe first)

Each item gives where the text is, what happened, how often, and a possible change. The Skill was not edited.

**D1. Straight apostrophes from expert results go into delegates unchanged.** SKILL.md line 44, check rule 2 (`’ for every straight apostrophe, in paths, names and the letter too`).
The model writes ’ in values it types itself, such as the album name in steps 1 to 3 and Q1. It copies paths, file names and model text that come back from experts as they are: step 4 paths (S1 2/2, S4 2/2), the step 6 name and the step 7 file name, letter and paths (S1 2/2, S4 2/2), the step 8 path (S1, S4), the Q3 file name and question line (S6 2/2), and `water's edge` from the vision answer in the step 7 letter (S7 2/2). 8 of the 10 runs whose expert results held a straight apostrophe broke this rule. The 2 that did not were S5, where the Q1 mock happened to return the photo path already written with ’, and the model copied it as it was. In a real single-quoted delegate, the first straight apostrophe would end the instruction early.
Possible change: make the experts return safe text, for example adding to the step 1, 2, 3, 6 and Q1 instructions `Write every straight apostrophe in returned names, paths and lines as ’.`, and to step 4 `... and in answer lines.` The parent then copies text that is already clean, which it does reliably. Keep rule 2 as a second guard.

**D2. Wrong numbered file name, and a failed save retried without a new save.** SKILL.md line 80 (`else base name, a dash and the first free number from 2, .txt`) and line 116 (`A failed or cancelled save is never repeated without a new save and approval from the helper.`).
S1 had the base name taken in both runs. Run 1 saved as `... 18-40, a dash and the first free number from 2, .txt`, copying the rule text into the file name. Run 2 first reused the taken name, which failed, then re-sent steps 6 and 7 without asking and saved as `... 18-40, dash 2.txt`. On the NAS, that retry would open a second approval dialog with no second save in chat. The model also did not show the approved letter after the failure (SKILL.md line 120, `If step 6 or 7 fails, show the approved letter in chat`).
Possible change: write the pattern out, for example `File name: {base name}.txt if free, else {base name} - 2.txt, then - 3.txt, the first that is free.` Next to step 7, add `If step 7 fails, show the letter, say why and wait for save; never send step 6 or 7 again on your own.`

**D3. Q2 sends names to the vision model.** SKILL.md line 100 (`What is visible: replace each name or family word with the position from the Family says line ...`).
S5 2/2 sent `what is Grandpa wearing?`, although the Family says line places Grandpa on the left. Because the question named a person, the mock returned UNCLEAR, and the listener got The photo cannot tell us that. The checks in Q2 are a bullet list and the rewrite is the last bullet, after the prompt instruction, so the model seems to skip it.
Possible change: make the rewrite its own numbered step just before the command and give the result a slot name, for example `Rewrite the question: Grandpa on the left gives what is the person on the left wearing. The question value must hold no name or family word.` Then use `{rewritten question}` in the question prompt sentence. The filled-instructions reference already has this example (`what is Grandpa holding`), but it did not carry over.

**D4. Identity question sent to the vision model.** SKILL.md line 98 (`Person question, ... Never call the vision model for it.`).
S6 run 2 sent `who is holding the baby?` to vision-vlm (1 of 2 runs). The prompt answered UNCLEAR in the mock, so nothing leaked here, but this is the one rule the tuning showed the prompt alone does not cover in Spanish, German or Turkish.
Possible change: put the person check before Q1, or begin Q2 with a single line such as `If the question starts with who, or holds a name or family word, do not send any command.` A short trigger is easier to follow than a long list.

**D5. Saved without the final save, and the letter changed after the preview.** SKILL.md line 76 (`After any change, show the full letter again. Save nothing before save; approval covers only the letter shown.`), line 67 and the step 7 command on line 83.
S4 run 1 went from an A1 answer straight to steps 6 and 7. In S4 runs 1 and 2, the first preview had no What this letter cannot tell you part and no photo files section, yet the saved file had both, so the approval covered a different text. In S1 run 2, the preview had a broken path (`Photo 7: /volume1/Photos/2026/IMG_4124.jpg`) while the saved text was correct. In S1 run 1, both the preview and the saved letter had a broken path for photo 6 (`/volume1/Photos/2026/80th birthday/IMG_4120.jpg`).
Possible change: in step 7, name the source of the text, for example `letter text = the last full letter shown in chat, copied unchanged`. Step 5 could add `A1 or a note is never a save; only the word save is.` Long path lists are copied badly, and nothing checks that the read-back paths match step 3.

**D6. The since notice is never shown.** SKILL.md line 67 (`add any notices that apply`), and the text sits only in letter-format.md lines 25 to 29.
S4 2/2 had no `Photos added later but taken before ...` line. The notice is defined only in the reference, and the step 5 preview template in SKILL.md has no place for it.
Possible change: put the notice line in the step 5 template, for example `{since notice, only in since mode}` after the first line, with the exact text in SKILL.md.

**D7. Letter folder from step 2 not used.** SKILL.md line 57 (`Keep: letter name and folder`) and line 79 (`folder = {letter folder or none}`).
S4 2/2 sent `folder = none` in step 6, although step 2 had returned the folder. The mock folder was the personal folder, so no harm showed here. With letters in a subfolder, the new letter would go to the personal folder, away from the earlier letter and its questions file.
Possible change: in step 2, write `Keep: letter name, letter folder (the folder of that letter), ...`, using the same words as the slot.

**D8. Q3 saves without save now.** SKILL.md line 111 (`Show the kept lines and ask: save now, or say more.`).
S6 2/2 went from `yes, keep it for the family` straight to the Q3 save command, without showing the kept line or asking. The platform dialog would still appear, but the chat step meant to collect more questions was skipped.
Possible change: `After yes, show the kept lines and stop. Send the Q3 command only after the words save now.`

**D9. Lines with no content are still read out.** letter-format.md line 16 (`each only when it has content`) and line 38 (`The listener never hears none.`).
Every letter in S1, S4, S7 and S8 had `Words in the photo: none.` lines, and S1 run 2 also had `Where: none.` lines. A screen reader reads the word none over and over. The step 4 instruction asks for `the vision-ocr result or none`, and the step 5 template uses `{... or none}`, so none reaches the letter.
Possible change: add to step 5 in SKILL.md: `Leave out a Where or Words in the photo line that would say none.`

**D10. Words from OCR marked as AI reading, and the long-number rule misapplied.** letter-format.md line 21.
S8 2/2 wrote `Happy Birthday (AI reading)` and `CALLE ESCORIAZA (AI reading)`, although vision-ocr had returned both words. In S1 photo 8, OCR returned `... PAST THIS POINT CALL 5550123`. Run 1 used the vision words with (AI reading), and run 2 used them with `and more text`, which is meant only for text over 25 words. Neither used the OCR words without the long number.
Possible change: give each case one short line, for example `vision-ocr text, not none: use it, no mark. vision-ocr none and a Words line: those words and (AI reading). Drop numbers of 5 or more digits and keep the rest.`

**D11. A Spanish listener gets English labels and an English date.** letter-format.md line 8 (`Other labels may be in the listener language.`).
In S8 (2/2), only the AI guess was in Spanish. When, Where, AI guess, Words in the photo, How to read it, What this letter cannot tell you and the date `20 July 2026` stayed English. The prompt language was right.
Possible change: say `must` instead of `may`, and give the labels in the listener language with an example date (`20 de julio de 2026`). Keep the English anchors.

**D12. Since mode can skip the setup message and pick the wrong prompt language.** SKILL.md line 11 and filled-instructions.md line 17.
S4 run 1 sent step 1 without the setup message, and its step 4 prompt said `in Spanish` for an English request about an English letter (1 of 2 runs). One possible cause is the Spanish example in filled-instructions.md (`Step 4a, brief detail, listener language Spanish`), together with Chilean place names in the results. This is not confirmed.
Possible change: state in Letter mode that the setup message is also sent for since requests. Make the synthetic example use English, or add `the language from setup line 2, never from place names`.

Smaller points:
- A reply that changes lines and says go got the setup message again instead of going on (S1 2/2; S7, which had the same kind of reply, went on). SKILL.md line 11 could say `A reply with go starts step 1 at once, changes included.`
- `the family says: Aunt Rosa ...` starts with a lowercase word when the helper is the default (S4 2/2), from the template `{helper} says:` in letter-format.md line 23.
- For an all-dark photo, the model wrote `This photo was not described. Reason: the photo is too dark and blurred to see.` and counted it as not described (S7 2/2). The rich prompt gives a Line 1 for this case, but the letter rules do not say how to show it. That is a reasonable result, but it is not specified.
- waiting_approval was paraphrased (file and folder kept) rather than shown unchanged (SKILL.md line 123). It is harmless here.
- `The question is: what is Grandpa wearing?.` gets a second full stop when the question ends with a question mark (vision-prompts.md line 15, `The question is: {question}.`).

## Harness limits
- The mocks are cooperative and quick. Real experts may return other fields, page differently, refuse long instructions or rewrite them. Approval dialogs are modelled as one message.
- The simulated user follows a script with one fallback (`Please go on.`). A real helper will phrase things differently.
- Checks are string and regex based. Each failure above was confirmed by reading the transcript.
- The model is a cloud stand-in. The real Uliya parent model, its delegate syntax and the NAS vision model are untested.

## After fixes (2026-10-31, second pass)

The Skill was edited after the review findings (source labels and letter wording, one-line delegates with ¶ for line breaks, experts asked to return ’, Q2 rewritten as numbered steps, Q3 wait, step 5 and 6 rules, setup defaults). The same harness was then run again on the scenarios that touch the changed parts. Raw transcripts: `app/tuning/results/sim_after/S*_r*.json`, log in `results/sim_after/run_log.txt`. The harness before this pass is kept as `results/sim/simulate_before_fixes.py.txt`; `patch_sim_after_fixes.py` holds the harness changes.

Harness changes, so the checks follow the new format: step 7 and Q3 texts are rebuilt from ¶; a line break is now flagged in every step; the opening line replaces the title line check; the reply check expects the spoken form (In the ... letter of 12 September 2026, photo N); the question prompt slot is {rewritten question}; step 3 mocks return the qualified count; the Spanish Not described check accepts no fue descrita. The mocks are cooperative: when an instruction asks the expert to write straight apostrophes as ’, the mock does so. That tests whether the parent copies the clean values, not whether a real expert would comply. Step 7 and Q3 now ask for the returned path with ’ too, but the mock does not honour that wording, so it was not exercised.

Budget: 40 model calls (32 in one live batch of S1, S4, S5, S6 and S8, then 8 in replays). Replays feed the recorded first turns back unchanged and run the model live from a later point, to retest one rule cheaply: S6 runs 2 and 3 from the user's yes, S8 runs 2 and 3 from the preview, S4 run 2 from the A1 answer. S6 run 3 and S4 run 2 stopped when the budget ran out (shown as API calls completed: false). S2, S3 and S7 were not run again. The system prompt grew from 52,435 to 62,861 characters in this pass, and one clause (old print openings in the listener language) was added after the live batch had started.

| Run | Kind | Critical checks | Verdict | What it shows |
|---|---|---|---|---|
| S1 r1 | live | 44/52 | FAIL | D2 fixed: file name `... 18-40 - 2.txt`, no retry. D1 fixed for every value copied from steps 1 to 6. No none lines (D9). First preview had no closing line and no photo files part, and said 8 of 8 instead of 8 of 14; the saved text had both parts. Step 8 path had a straight apostrophe from the step 7 result (step 7 fixed afterwards). |
| S4 r1 | live | 25/28 | FAIL | D6 fixed: since notice shown. D7 fixed: step 6 used the letter folder. Setup message skipped again (D12) and A1 went straight to step 6 (D5). Both rules were rewritten after this run. |
| S4 r2 | replay from A1 | 14/18 | cut by budget | D5 fixed in this run: after A1 the full preview came back and step 6 waited for save. The re-shown preview again had no photo files part. Setup failure is from the replayed turn, not retested. |
| S5 r1 | live | 14/14 | PASS | D3 fixed: the vision model got what is the person on the left wearing, with no name. |
| S6 r1 | live | 12/13 | FAIL | D4 fixed: no vision call for who is holding the baby. D8 still open: Q3 saved right after yes. |
| S6 r2 | replay from yes | 12/13 | FAIL | Same D8 failure after the first Q3 rewrite (kept-lines template). |
| S6 r3 | replay from yes | 13/14 | cut by budget | D8 fixed after the second rewrite (a yes is not a save): kept line shown, save only after save now, right file name and folder. The final chat line after the save was not generated. |
| S8 r1 | live | 21/21 | PASS | OCR words used for photo 2; photo 3 still marked AI reading although vision-ocr confirmed it. Labels stayed English. |
| S8 r2 | replay from preview | 16/21 | FAIL | After the labels rule moved into SKILL.md, the whole letter came out in Spanish, but the For the helper part was translated too, so the anchors broke. |
| S8 r3 | replay from preview | 21/21 | PASS | After the anchors were listed one by one, they stayed English, but the listener labels went back to English. |

Pass rate after fixes: 3 of 10 runs pass every critical check (S5 r1, S8 r1, S8 r3), and 192 of 215 critical checks pass (89 percent). Before this pass, the same five scenarios passed 227 of 257 critical checks (88 percent) and 2 of 10 runs. The check sets differ slightly between the two passes, so the two figures are not strictly comparable. One run per changed rule at temperature 0.2 is a smoke test, not proof.

Closed in at least one run after the last edit to that rule: D1 (for values copied from steps 1 to 6 and Q1), D2, D3, D4, D5 (A1 is not a save), D6, D7, D8, D9.

Still open or not retested:
- Preview without the photo files part: 2 of 4 previews after this pass (S1 r1 before the template change, S4 r2 after it).
- Setup message skipped in since mode (S4 r1). The workflow line now says so explicitly; not retested live.
- D11, listener language: 1 of 3 Spanish previews had Spanish labels, and that one translated the anchors too. Not solved.
- New defect from the spoken time format: 11:20 was written as 11:20 in the evening (S4 r1, repeated in r2). An hour table was added to the letter format reference; not retested.
- D10: vision-ocr confirmation applied in 3 of 5 confirmed cases; photo 3 in S8 and photo 8 in S1 were still marked AI reading, which is the safe side.
- The old print When rule (copied or scanned on) was never applied (S1 photo 7, S8 photo 1).
- Q3 wrote asked by your relative although the user named Grandpa (S6 r3).
- An answered question was still listed in the Open questions line of the preview (S4 r2), though not in the letter.
- Whether the real runtime accepts a delegate of several KB on one line, and whether knowledge-agent turns ¶ into line breaks, is unknown. The harness rebuilds the text itself.

## Third pass (2026-11-01): full rerun, fixes, rerun

The second pass above only replayed parts of five scenarios. This pass ran every scenario from the start with the Skill as shipped on 2026-10-31, fixed what failed, and ran everything again. Same model, temperature, mocks and checks. Raw transcripts and logs: `results/sim_v4_base/`, `sim_v4_fix1/` to `sim_v4_fix3/`, `sim_v4_final/` and `sim_v4_s1check/`. The Skill before this pass is kept as `results/SKILL_before_v4.md.txt`.

**Baseline, Skill of 2026-10-31, 8 scenarios × 2 runs:** 8 of 16 runs clean, 303 of 317 critical checks.

| Defect seen in the baseline | Runs | Change |
|---|---|---|
| A family note with a straight apostrophe (Grandpa's dog) went into the step 7 command unchanged | S1 2/2 | Step 5 writes ’ in Family says lines; the step 7 letter text slot says every straight apostrophe becomes ’ |
| Step 8 copied the output path from the step 7 result, which held a straight apostrophe | S1 2/2 | Step 8 reads the folder and file name the Skill sent in step 7, with a fallback to the newest file starting with that name |
| Preview said 8 of 8 photos chosen instead of 8 of 14 | S1 2/2 | Preview line rewritten as {K} photos qualified, {M} chosen |
| The A1 answer was shown after the letter, or dropped, and never saved | S4 2/2 | Step 5 gives the exact Answers from the family line and says it goes before the closing line |
| After a denied save, the letter was not shown again | S7 1/2 | Fixed reply: Nothing was saved. Here is the letter again; say save to try again. and the letter |
| The rich prompt lost its old print sentence when copied | S7 2/2 | The clear-detail clause moved into the Line 2 sentence, so the rich prompt has the same shape as the brief one |
| A question reply did not start with the letter and photo | S5 1/2 | The reply rule says two lines: the In the ... letter ..., photo N. line, then exactly one answer line |
| Setup message skipped when the request gave every value | S1 1/2 | First reply is always the setup message, never a command |
| Eight photos sent in one vision command | S1 1/2 (fix 2) | Step 4 spells out one command per group of 4 |

One change made things worse and was reverted: moving the Q2 opening line out of its header made the model skip the vision call (S5 2/2) and send an identity question to vision (S6 2/2), see `sim_v4_fix1/`.

Harness changes in this pass, so the checks follow the new wording: the step 8 mock and check accept folder plus file name; the preview count check accepts 14 photos qualified, 8 chosen.

**After the first fixes:** 21 of 22 runs clean, 432 of 433 critical checks (`sim_v4_final/`, `sim_v4_s1check/`). The one failure: in S4 run 1 the Answers from the family part was saved after the photo files section.

**Question mode broke again in a recheck.** After a one-sentence change to the question prompt (step 3, see `RESULTS.md`), question mode failed 3 of 4 runs (`sim_v4_qcheck/`): after yes, the model looked up and saved the questions file without save now (S6 2/2), and once answered a what-is-visible question from the AI guess line with no vision call (S5). The same Skill text had passed 6 of 6 before, so question mode is sensitive to small changes. Q3 was rewritten as numbered sub-steps (yes is not a save, no command in that reply; save only after save now; no lookup after Q1), and Q2 step 3 now says the answer must come from the vision model. A full run then showed S5 still filling all four reply lines at once (`sim_v4_release/`, 2/2), so the reply template went back to four alternatives with exactly one of the four lines, never two.

**Final package (the ZIP as shipped):** 23 of 24 runs clean, 419 of 421 critical checks.
- Letter mode, S1 to S4, S7 and S8, 2 runs each: 12 of 12 clean, 264 of 264 checks (`sim_v4_release/`). These ran before the last edit, which changed only the question mode reply wording in Q2.
- Question mode, S5 and S6, 6 runs each, on the final text: 11 of 12 clean, 155 of 157 checks (`sim_v4_q4/`). The failure: S5 run 1 answered from the family notes and the AI guess line instead of calling the vision model.
- A last full rerun of all scenarios on the final text stopped when the API account budget ran out; it is kept, unused, in `sim_v4_release2_DISCARDED_api_budget/`.

Seen in single runs during this pass and not fixed: a one-word copy slip in the brief prompt (who became a), and one preview where the model repeated a block of the letter; the saved text was correct in that run.

What this still does not show: the mocks are cooperative and hand-written, the parent is a cloud stand-in, and nothing ran on a NAS. 24 runs at temperature 0.2 is a smoke test, and question mode in particular moved with small wording changes. Model calls in this pass: about 800, until the account budget ran out.
