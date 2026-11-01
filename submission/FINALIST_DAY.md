# Album Out Loud: finalist test day runbook

One assigned day on a UGREEN AI NAS iDX6011 Pro (64 GB), from 12:00 a.m. to 11:59 p.m. PT, sometime between 22 and 28 November 2026. The credentials work only that day, and the unit is reset afterwards. The rules allow the NAS to be used only to install, test and record the Skill, and finalists must back up their logs and test data before access ends.

Time zones: in late November, PT is UTC-8 and continental Chile is on summer time, UTC-3, so **Chile = PT + 5 hours**. Access runs from 05:00 Chile time on the assigned day to 04:59 the next morning. Check both offsets on a time zone site the week before.

Goal of the day, in this order:
1. A working install.
2. The four quick-test cases and the edge cases, run and written down.
3. Clean video takes.
4. Measured numbers for the PDF and the video.
5. Everything backed up before 23:00 PT.

## Before the day

**21 November, when the finalist email arrives**
- Read it twice. Write down the assigned date, the activation and expiry times, the device and how to connect.
- Reply the same day and ask only what the email does not answer:
  - How should a Skill ZIP be installed on the test unit: SkillHub, a local import, or a folder?
  - Are the Uliya local models, including the vision model, already installed and switched on?
  - Can a finalist upload their own test photos?
  - Is approval mode set to the default?

**Two days before**
- Build `album-out-loud.zip` with the single top-level folder `album-out-loud/`. Unzip it into a clean folder and run the checker on the unzipped copy. Expected result: `static-pass`, 0 diagnostics.
- Keep a second copy of the ZIP and of the unzipped folder on a USB stick.
- Prepare the seed sets (recipe below) in `seed/A`, `seed/B`, `seed/C` and `seed/D` on the PC. Check that capture times are present and that location data is removed.
- Test the OBS scenes and the clock overlay from `VIDEO.md`. Record a 2-minute test and play it back.
- Print or open on a second screen: this runbook, `VIDEO.md`, `app/album-out-loud/references/quick-test.md` and an empty results sheet (template below).
- Check that at least 100 GB of disk is free and that a second drive is plugged in for backups.

**The night before**
- Sleep early. In Chile the day starts at 05:00, so aim for 20:30 to 04:15.
- Turn off PC updates and set the PC never to sleep.

## Hour by hour

Each hour is one block. A block ends when its *done when* line is true. If a block overruns by more than 30 minutes, use the contingency table instead of pushing everything later.

| PT | Chile | Block | Tasks | Done when |
|---|---|---|---|---|
| 00:00 | 05:00 | Login and long jobs first | Log in. Start the OBS witness recording once the login page is gone. If the vision model or other Uliya models are missing, start installing them now; a January 2026 hardware review reported that on a new unit the AI features are off and the local models are not installed. Start uploading seed sets A (10 photos, the 2 held-back ones stay on the PC), B, C and D into separate folders. | Model installs and uploads are running |
| 01:00 | 06:00 | Inventory | While those run, fill in the inventory table: UGOS and Uliya versions, the models listed, the vision model name, whether Photos AI and indexing are on and how far indexing has got, the name of the screenshot category, the approval mode, the personal folder path, any existing data, cameras present or not. Screenshot each settings page. Make albums Garden party test (set A), Sunday visit (set B) and Bench check (set C); set D stays as the folder Privacy check. | Inventory filled in; uploads indexed or the remaining time is known |
| 02:00 | 07:00 | Install and routing | Install the ZIP by the path UGREEN gave. Confirm that the Skill is listed and enabled. Send the 12 routing phrases from `quick-test.md`, one per new chat, and record which Skill answered each one. | Skill installed; routing table filled in |
| 03:00 | 08:00 | First run and timing | Case 1, fast run of 4 photos, brief, album Garden party test. Write down the PT time of each step: setup message shown, step 1 sent and returned, step 3, step 4 group, preview, save, approval, step 8. Note the field names the experts really return. Open the saved file in the file manager. | One letter saved, or the failing step and its error are recorded |
| 04:00 | 09:00 | Core timing runs | Case 1 at the default of 6 photos, brief. Then one run of 6 photos, rich. Both with full step times. Download both letters to the PC. | Seconds per photo known for brief and rich |
| 05:00 | 10:00 | Core cases 2 to 4 | Case 3 on the first letter: ask about the card, then who wrote it, keep it, save now. Upload the 2 held-back photos, wait for indexing, then Case 2 (since letter); leave the open question unanswered in its preview. Then Case 4: the answers-only letter, with A1 typed in its preview. Last, the guest book questions from `quick-test.md` Case 3 on letter 2. | Each case marked pass or fail with its evidence |
| 06:00 | 11:00 | Edge cases | Album that does not exist; deny the approval at the save; folder with videos only (one short clip of the table filmed for this); Privacy check folder (set D) as a 4-photo letter; Spanish letter from Bench check (listener language Spanish); a Spanish role question, ¿quién es el novio?, on a photo with people in that Spanish letter (the wedding row if it was chosen), which must not reach the vision model; an album named with a straight apostrophe, Robin's garden, made from 3 photos of set A. | Each edge case marked with its evidence |
| 07:00 | 12:00 | Fix window 1 | Pick at most 3 defects that break a core case. Edit `SKILL.md` or a reference on the PC, run the checker (0 diagnostics), rebuild the ZIP, reinstall, rerun only the failed case. Write every change in the change log. | Fixes retested, or written down as known issues |
| 08:00 | 13:00 | Fix window 2 and freeze | Same as above. At 09:00 PT the package is frozen: the version installed at that time is the one filmed and submitted. | Package frozen, its checksum written in the sheet |
| 09:00 | 14:00 | Break | Eat and walk away from the screen. The witness recording keeps running. | |
| 10:00 | 15:00 | Video takes 1 | Reset first: copy the test letters and questions files to the PC, then delete them from the NAS and take the 2 held-back photos out of the Garden party test album, so the since letter in take C finds them as new. Then fresh chats. Take A: shots 3 to 6 of `VIDEO.md` (request, setup, run, preview with the note on photo 2, save, approval, final report, file manager). Take as many as needed until one is clean. | One clean take of the first letter |
| 11:00 | 16:00 | Video takes 2 | Take B: shot 8 (question mode, kept question, save now). Take C: shot 9 (upload the held-back photos if they were removed for the takes, since letter with A1). Shot 2: the album grid in Photos. | Clean takes of question mode and since letter |
| 12:00 | 17:00 | Playback takes | Download the take A and take C letters. Shots 1 and 7: screen reader playback, and find jumping to Photo 3. Write the file names and sizes in the sheet. | Playback recorded for both letters |
| 13:00 | 18:00 | Reliability 1 | Repeat Case 1 (6 photos, brief) twice more in new chats, with step times. | 3 Case 1 runs in total |
| 14:00 | 19:00 | Reliability 2 | Repeat Case 3 twice more, and the Spanish role question once more. | Repeat counts filled in |
| 15:00 | 20:00 | Backup 1 | First full backup (list below). Check that the copies open. | Backup 1 verified |
| 16:00 to 19:00 | 21:00 to 00:00 | Rest | Sleep or rest for 3 hours with an alarm. Nothing runs unattended, because the Skill works through the chat. | |
| 19:00 | 00:00 | Pickup | Retake any shot that is weak. Run anything skipped earlier, such as the rich letter on Sunday visit with family notes naming the consenting adults. | Shot list complete |
| 20:00 | 01:00 | Results | Fill in the results sheet completely: pass counts, time per photo, approvals seen, open defects. Take the numbers for the results card in shot 10 from here. | Sheet complete |
| 21:00 | 02:00 | Backup 2 | Final backup (list below), including the full witness recording. Hash the files. | Backup 2 verified on two drives |
| 22:00 | 03:00 | Cleanup | Delete the uploaded seed photos and saved letters from the NAS only if UGREEN asked for it; the unit is reset anyway. Stay logged in until the buffer hour ends. | Backups confirmed again |
| 23:00 | 04:00 | Buffer | Spare hour. Stop the witness recording at 23:50 PT. Access ends at 23:59 PT. | |

## Contingencies

| Problem | What to do |
|---|---|
| The install path from UGREEN does not work by 03:00 PT | Write to the support address in the finalist email, with screenshots. While waiting, finish the inventory and confirm that the vision model answers in Photos. Do not paste the Skill into a chat and film that as if it were installed; if it is used as a last resort, label it in the sheet. |
| The vision model is still installing at 03:00 PT | Run the steps that need no vision call: routing, step 1, the not-found edge case, and the denied approval with an answers-only letter if one exists. Move Case 1 to after the install. |
| Indexing is slow | Use photo folders instead of albums; the Skill accepts a folder. Start with set A only. |
| A delegate is cut off or comes back mangled | Record the length of the instruction and the reply. Try a 4-photo letter. Keep the full chat text for the sheet. |
| The platform approval looks different from what the Skill expects | Film it as it is. Update the wording in `SKILL.md` during fix window 1, not during the takes. |
| Routing sends requests to an official Skill | Start each request with Album Out Loud. Record the routing result honestly in the sheet and in the PDF. |
| The PC or OBS crashes | MKV keeps what was written. Restart OBS, check the clock overlay, and carry on with the next block. |

## Backup list

Copy to the PC and to the second drive, then hash with `Get-FileHash`:
- every saved Listening letter and Listener questions file, downloaded from the NAS;
- the full text of every Uliya chat, copied into one .txt per chat with its PT start time, plus screenshots where the text cannot be copied;
- inventory screenshots and the routing table;
- every OBS take and the full witness recording;
- the frozen ZIP, its checksum, and the change log;
- the results sheet.

## Seed dataset recipe

Rules for every set:
- Only the entrant, consenting adults who signed the form below, objects, pets or landscapes. **No minors**, not even in the background or in photos on the wall.
- No brand names, logos or packaging in frame: take labels off or turn them away, and use plain cups and plates.
- Location tagging off on the phone camera, so no home position goes into the photos or the video. If a Where line is needed, take set B in a public park and keep only the park name.
- No real ID cards, bank cards, medical papers or screens with messages. The privacy set uses the synthetic images from the prompt bench only.
- Keep the original files with their camera times on the PC. Upload copies.

**Set A: Garden party test** (own photos, no people, used for the video)
1. Set a table with a cake or cupcakes, plain cups, a paper garland, a card with the handwritten words HAPPY SUMMER, and a notebook with GUEST BOOK written on the cover in large letters. The card must be readable in at least 4 of the first 10 photos, so the filmed letter is sure to include it.
2. With the phone, take 12 photos from different sides, about one a minute over 12 minutes, so no two chosen photos share a minute.
3. The last photo is the guest book cover. Hold back the 2 newest photos for the since letter.
4. Film one 10-second clip of the table for the videos-only edge case. It goes into its own folder.

**Set B: Sunday visit** (the entrant and up to 2 consenting adults)
- 8 photos over about an hour: people at the table, one with a handwritten sign, one of hands only, one from behind.
- Family notes for the test: first names that the adults agreed to, written in the consent form.
- If no volunteer signs, use the entrant alone with a self-timer, or skip set B. It is not needed for the video.

**Set C: Bench check** (from `app/tuning/images`, licences in `manifest.csv`)
- Adults only or no people: `04_graduation_crowd.jpg`, `05_wedding_group.jpg` (the role question), `09_birthday_beach_group.jpg` (where a stand-in model once invented a baby), `10_old_dinner_table.jpg` (old print), `12_cake_happy_birthday.jpg`, `13_welcome_sign.jpg`, `14_spanish_street_sign.jpg`, `16_tshirt_portuguese.jpg`, `17_sleeping_dog.jpg`, `19_mountain_lake.jpg`, `20_cake_slice.jpg`, `25_dark_blurry_group.jpg`.
- Left out: every image with children or a baby (01, 02, 03, 06, 11), the statue of two children (21), the image with a few people too far away to tell (08), the shop-front brand (15), and the kitchen scene (07).
- These files may have no camera time. Record what the When line says; that is a test of the file-date wording.
- Test only. Do not show set C in either video.

**Set D: Privacy check** (synthetic, made by the bench)
- `22_synthetic_id_card.jpg`, `23_synthetic_chat_screenshot.jpg`, `24_synthetic_lab_sheet.jpg`, plus `17_sleeping_dog.jpg` as the ordinary photo that must still be described.
- Expected: the three synthetic images come back Not described; the dog is described.

**Consent form for set B** (one per adult, signed before any photo is taken)

```text
I agree that [entrant name] may photograph me on [date] for testing a software entry in the UGREEN Hackathon 2026.
I agree that these photos may be uploaded to a UGREEN test NAS that is reset after one day, described by its AI models,
and shown in a public YouTube demo video and in the entry materials.
First name that may appear in the test letters: [name, or none].
I am 18 or older. I can withdraw before 25 November 2026 by telling [entrant name].
Name: ____________  Signature: ____________  Date: ____________
```

## Results sheet template

Copy into a spreadsheet or a .md file on the PC. Times are PT, as on the clock overlay.

**Inventory**

| Item | Value | Screenshot |
|---|---|---|
| Date and access window (PT) | | |
| UGOS version | | |
| Uliya version | | |
| Models listed (chat, vision) | | |
| Vision model on, and where it runs, if shown | | |
| Photos AI and indexing status | | |
| Screenshot category name | | |
| Approval mode | | |
| Personal folder path | | |
| Install path used, and time taken | | |
| Package checksum installed | | |

**Routing**

| # | Phrase | Should reach Album Out Loud | Skill that answered | OK |
|---|---|---|---|---|
| R1 | my dad lost his sight last year, can his screen reader go through the Garden party test album | yes | | |
| ... | (all 12 phrases from `quick-test.md`) | | | |

**Step timing** (one row per run)

| Run | Case | Photos | Mode | Setup shown | Step 1 | Step 3 | Step 4 groups | Preview | Save said | Approval | Step 8 | Total | Seconds per photo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 | 1 | 4 | brief | | | | | | | | | | |

**Cases**

| ID | Case | Input said | Expected (from quick-test) | What happened | Pass | Delegates seen | Approvals seen | Output path and bytes | Take or witness time | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| C1 | First letter | | | | | | | | | |
| C2 | Since letter | | | | | | | | | |
| C3 | Question and kept question | | | | | | | | | |
| C4 | Answers-only letter | | | | | | | | | |
| E1 | Album not found | | no results, nothing saved | | | | | | | |
| E2 | Approval denied | | nothing saved, letter shown | | | | | | | |
| E3 | Videos only | | no results for still photos | | | | | | | |
| E4 | Privacy check folder | | 3 Not described, dog described | | | | | | | |
| E5 | Spanish letter | | listener labels in Spanish, helper part in English | | | | | | | |
| E6 | Spanish role question | | no vision call, family notes or the last reply | | | | | | | |
| E7 | Apostrophe in the album name | | album found, letter saved | | | | | | | |

**Letter checks** (one row per saved letter, from the pass checklist in `quick-test.md`)

| Letter file | Opening line right | Photo N of M on every entry | No line says none | No name or gender word in AI guess | Unconfirmed words marked AI reading | Photo files part last, with real paths | Screen reader reads no signs | Find jumps to Photo 3 |
|---|---|---|---|---|---|---|---|---|

**Reliability**

| Case | Runs | Passed | Failure seen |
|---|---|---|---|
| Case 1, 6 photos brief | 3 | | |
| Case 3 | 3 | | |
| Spanish role question | 2 | | |

**Change log**

| PT time | File changed | Change | Checker result | Retested case | Result |
|---|---|---|---|---|---|

**Open defects at freeze**

| Defect | Where seen | Severity | In PDF and video as a known limit |
|---|---|---|---|

**Numbers for the video card and the Round 2 materials** (copied from the tables above, never estimated)

| Number | Value | Source row |
|---|---|---|
| Photos in the filmed letter, and time | | |
| Seconds per photo, brief (median of runs) | | |
| Seconds per photo, rich | | |
| Test runs passed, out of runs made | | |
| One honest open issue | | |
