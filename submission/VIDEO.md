# Album Out Loud: video plan

Two videos are planned here.

1. **Round 2 demo** (required for finalists): under 3 minutes, English narration, public on YouTube. Every NAS shot is recorded on the assigned test day.
2. **Round 1 concept walkthrough** (optional, 60 to 90 seconds): only artifacts that already exist. There is no NAS footage in it, and it says so.

## What the rules require (Round 2)

From the official rules and the Devpost overview page:
- Less than 3 minutes. Judges do not have to watch past 3:00. Target length: 2:50.
- It must show the Skill running in the UGREEN AI NAS test environment, with narration that explains the core workflow, the key capabilities and the actual results.
- Record the Skill on the assigned NAS during the assigned testing day.
- English narration, or complete English subtitles. Plan: both.
- Public on YouTube, with the link in the Round 2 form. Deadline: Monday 30 November 2026, 11:45 pm PT.
- No third-party trademarks, copyrighted music or other material without permission. UGREEN marks and materials UGREEN provides are allowed.
- The assigned NAS may be used only to install, test and record the Skill.

What this means in practice:
- No music at all. The only sounds are the narration and the screen reader voice.
- Nothing appears on screen except the UGOS web interface, a plain text window and the clock overlay. No browser tabs, bookmarks bar, extension icons, taskbar, OS logos, editor or screen reader branding.
- In the narration, say "a screen reader" and "a text editor", never product names.
- Seed photos show no brand labels, logos or packaging (see the seed recipe in `FINALIST_DAY.md`).
- Never claim a blind tester. The playback shot is labelled as the entrant listening.

## Run order to film (differs from `quick-test.md` on purpose)

The video tells one continuous use, so the cases are filmed in this order, all on album **Garden party test** (Set A, no people):

1. First letter for Dad, 6 photos, brief. Photo 2 gets a note. Save and approve.
2. Question mode on the first letter: one visible question, then one the photo cannot answer. Keep it, say save now, approve.
3. Upload the 2 held-back photos. Since letter: only the 2 new photos, plus the answer to the kept question typed as A1. Save and approve.

The quick-test order (since before question) is still run for the results sheet, separately.

## Timestamped script

The narration is about 350 words, which fits 2:50 at a calm pace. Text in {braces} is filled from the results sheet on the day. Never fill it with an estimate.

| Time | On screen (action) | Narration (English) |
|---|---|---|
| 0:00 to 0:10 | Cold open. Saved letter in a plain text window, large font. The cursor moves line by line while the screen reader reads Photo 2 aloud: number, When, Family says, AI guess, Words in the photo. Caption: *A screen reader reading a letter saved on the UGREEN AI NAS test unit, {date} PT.* | none, only the screen reader voice |
| 0:10 to 0:26 | Title card: Album Out Loud, a Uliya Skill. Then a slow pan over the album grid in UGOS Photos. Clock overlay visible. | A phone can describe one photo. It cannot tell a blind grandparent who is in it, or why the day mattered. Album Out Loud turns a family album on a UGREEN AI NAS into a letter they can listen to, and every line says where it came from. |
| 0:26 to 0:40 | Uliya chat. The helper types: *Album Out Loud, make a listening letter for Dad from the album Garden party test.* The setup message appears with its six numbered lines. The helper types *go*. | The helper asks once. Uliya answers with one setup message, already filled in: the album, who it is for, the language, the detail and six photos. I reply go. |
| 0:40 to 1:05 | The run, shown as a time-lapse. Each delegate appears with a short caption: *find the album*, *choose 6 of {K} photos*, *describe photos 1 to 4*, *photos 5 and 6*, *find a free file name*. Corner label: *real time {mm:ss}, shown at {N}x*. | The Skill hands the work to the NAS experts. The photo expert finds the album, picks six photos spread across the afternoon, reads their camera times and runs the vision model of the NAS on each photo with a fixed prompt. Nothing in Photos is changed. |
| 1:05 to 1:30 | The preview, scrolled slowly. The helper types *2: the cups from the holiday*. The full preview comes back with a Family says line on photo 2. The helper types *save*. The platform approval appears and is accepted. | Before anything is saved, the helper reads the whole letter. Notes go in by photo number, and they come before the AI guess. Names only ever come from the family. The helper says save, then confirms once more if the platform asks. That is the only write for the letter. |
| 1:30 to 1:45 | Final report: *Saved and checked: {path}, {bytes} bytes, 6 photos, {X} not described.* Cut to the UGOS file manager with the new .txt file selected. | The file is read back and compared before Uliya calls it saved. It is a plain text file in the helper's own folder on the NAS. |
| 1:45 to 2:05 | The file downloaded to the PC and open in a plain text window. The screen reader reads the opening lines, then find jumps to *Photo 3 of 6*. Caption: *The entrant listening. No blind or low-vision tester took part.* | Every entry starts with its number, so the listener can jump straight to photo 3. Family says lines are from the helper. AI guess lines were written by a computer and may be wrong, and the label says so before the guess does. |
| 2:05 to 2:30 | Uliya chat: *Album Out Loud, photo {n} of the Garden party test letter, what words are on the card?* The reply starts with *AI guess, may be wrong*. Then: *who wrote this card for Dad?* Reply: *The photo cannot tell us that. Shall I keep the question for the family?* The helper types yes, then save now, and accepts the approval. | Through the helper, the listener can ask about one photo. What the vision model can see, it answers, marked as a guess. Who wrote the card, no photo can say, so the question is kept for the family. |
| 2:30 to 2:42 | Time-lapse of the since letter. The preview says *2 of 2 photos chosen*. The helper types *A1: the neighbours, for his birthday*. The saved letter shows *Answers from the family*. | Next time, the letter covers only the new photos, and it brings the family answer with it. |
| 2:42 to 2:52 | Results card, plain text on a dark background: *Measured on {date}, iDX6011 Pro: {M} photos in {mm:ss}; {x} of {y} test runs passed; still open: {one honest line}.* End card: *Album Out Loud. Family first, one save, every line labelled.* | These are the numbers from the test day, including what did not work. Album Out Loud: the family first, one save, and every line says where it came from. |

If the platform approval never appears, change the 1:05 line to "The helper says save" and drop "confirms once more". If a photo comes back Not described, keep it in the shot and add the line "A photo the model cannot describe safely says so instead of guessing."

## Shot list

| # | Time | OBS scene | Content | Audio | Filmed on NAS day | Fallback if the take fails |
|---|---|---|---|---|---|---|
| 1 | 0:00 | Playback | Saved letter in a plain text window, screen reader reading Photo 2 | screen reader | yes, after the step 8 save | Use the take from shot 7 |
| 2 | 0:10 | Title, then NAS browser | Title card, then the album grid in Photos | narration | the grid: yes; the title card is made after | Still image of the grid from the same day |
| 3 | 0:26 | NAS browser | Uliya chat: request, setup message, go | narration | yes | Second take from the reliability runs |
| 4 | 0:40 | NAS browser | Delegates running, time-lapse with speed label | narration | yes, recorded in real time | Use the take where every group returned |
| 5 | 1:05 | NAS browser | Preview, note on photo 2, save, platform approval | narration | yes | Any clean take; the note text must match the shot 7 file |
| 6 | 1:30 | NAS browser | Final report line, then the file in the file manager | narration | yes | Screenshot plus a short pan |
| 7 | 1:45 | Playback | Downloaded file, screen reader, find Photo 3 | screen reader, then narration | yes, the same day | Re-record the playback the same day from the backup copy |
| 8 | 2:05 | NAS browser | Visible question about the card, then an unanswerable one, keep, save now, approval | narration | yes | Use the Case 3 take from the results runs, captioned as a separate run |
| 9 | 2:30 | NAS browser | Since letter: 2 new photos, A1 answer, saved letter | narration | yes | Time-lapse of the Case 2 and Case 4 takes, captioned as separate runs |
| 10 | 2:42 | Card | Results card from the results sheet, then the end card | narration | the numbers come from the day; the card is made after | none needed |

Rules for editing:
- A speed-up always shows its real duration and its factor.
- Cuts inside a run get a one-frame dip and the caption *cut, {mm:ss} skipped*. Never splice two runs together as if they were one; if shots come from different runs, the caption says so.
- The clock overlay stays visible on every NAS shot, so the date and time are never in doubt.
- Narration is recorded after the day, over the footage of the day. The video description says so.
- Captions: an English .srt with every narrated line and every caption, uploaded to YouTube as complete English subtitles.

## Recording setup

**OBS scenes**
- *NAS browser*: window capture of a clean browser profile with no extensions, bookmarks or other tabs, cropped to the page content. Browser zoom 125 percent so the chat text can be read at 1080p.
- *Playback*: window capture of a plain text editor with large type (24 pt or more), cropped to the text area so no app name or icon shows, plus desktop audio for the screen reader voice.
- *Title* and *Card*: a colour source and a text source. No images from outside the project.
- A clock overlay on every scene except Title and Card.

**On-screen clock.** A Text (GDI+) source with *Read from file* on, pointing at a file that a small PowerShell loop rewrites every half second. Run it in a separate window before opening OBS:

```text
while ($true) { $pt = [System.TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([DateTime]::UtcNow, 'Pacific Standard Time'); ('PT ' + $pt.ToString('yyyy-MM-dd HH:mm:ss') + '   assigned test day') | Set-Content -Encoding utf8 $env:USERPROFILE\obs-clock.txt; Start-Sleep -Milliseconds 500 }
```

Show PT, because the testing day runs from 12:00 a.m. to 11:59 p.m. PT. Bottom right corner, white text on a semi-transparent black box, about 28 px.

**Output settings**
- 1920x1080 at 30 fps, recorded as MKV (it survives a crash), remuxed to MP4 for editing.
- Quality-based encoding at about CRF/CQ 20. Check that at least 100 GB is free before the day.
- Audio track 1: desktop audio (screen reader). Track 2: microphone, muted all day.
- Two recordings at once:
  - a low-bitrate *witness* recording of the whole session, started at the first login and never stopped, as evidence and backup;
  - separate high-quality *takes* for each shot.
  The Source Record plugin, or a second OBS profile, can do this. If neither is available, make the takes the priority and keep each one as its own file.

**Before every take**
- Notifications off (focus mode), taskbar hidden, other windows closed.
- The credential email, login page and any password field are never on screen. Start recording after login.
- The clock overlay shows the right PT time.
- Say the take number out loud on the muted mic track, or type it in the results sheet with the PT time.

**Screen reader playback.** Download the saved .txt from the NAS through the UGOS file manager, open it in the plain text editor, and let the screen reader read it with its default voice and settings. Record it on the day, and note the file name and size in the results sheet so the file can be matched to the NAS save.

**YouTube**
- Public, not unlisted.
- Title: *Album Out Loud: a listening letter from a family album on UGREEN AI NAS*.
- The description says: recorded on {date} on the assigned iDX6011 Pro; time-lapses are labelled with real time; narration was recorded afterwards; no blind or low-vision tester took part; the seed photos are the entrant's own or consenting adults.

## Round 1 optional concept walkthrough (60 to 90 seconds)

Round 1 does not ask for a video. Make this only if the form has a field for one and there is time left after the PDF and the ZIP. It uses only artifacts that exist today. There is no NAS footage, no mock-up of UGOS and no voice pretending to be a user.

| Time | On screen (real artifact) | Narration (English) |
|---|---|---|
| 0:00 to 0:12 | The synthetic example letter from `references/letter-format.md`, pasted into a plain text window and read by a screen reader on the PC. Caption: *Synthetic example letter from the Skill package. Not produced on a NAS.* | This is what Album Out Loud is meant to produce: a plain-text letter from a family album, for a relative who listens with a screen reader. |
| 0:12 to 0:27 | Slow scroll through `SKILL.md`: the setup message, then the delegate lines to photo-agent, file-agent and knowledge-agent. | The Skill is Markdown only. It asks one setup question, then hands the work to three NAS experts: photos, files and the save. Family notes come before the AI guess, and the helper approves one save. |
| 0:27 to 0:37 | Terminal, cropped to the text: the official checker run on `app/album-out-loud`, ending in `static-pass` with 0 diagnostics. | It passes the official static checker with no diagnostics. |
| 0:37 to 0:57 | The bench: CC0 image `14_spanish_street_sign.jpg` (Alavense, Wikimedia Commons). Two recorded outputs side by side for a Spanish request. First prompt: *A blue street sign hangs from a metal pole on a cloudy day.* Revised prompt (round 1 variant B): *Una señal azul indica la Calle Escoriaza junto a un poste y un árbol.* Then the synthetic ID card `22_synthetic_id_card.jpg` with *Not described: ID card with personal data.* Caption: *Cloud stand-in model, not the NAS model.* | I tuned the vision prompts with cloud stand-in models on 25 public-domain, CC0 or synthetic images, plus two more in a review, never family photos. The first prompt answered Spanish requests in English. Naming the language on every line fixed that. ID cards stayed Not described in every test. |
| 0:57 to 1:10 | The after-fixes table from `app/tuning/SIMULATION.md`, with the row *23 of 24 runs clean, 419 of 421 critical checks* highlighted. | A cloud model then played the Uliya parent agent against expert replies I wrote by hand. It found real bugs: half the runs failed at first. After three rounds of fixes, 23 of 24 runs were clean, against cooperative replies, not real experts. |
| 1:10 to 1:20 | End card, plain text: *Nothing in this video ran on a UGREEN NAS. If selected, the real run is recorded on the assigned test day.* | None of this ran on a NAS yet. If selected, the real test happens on the assigned day. |

Rules for this variant:
- Show only CC0 images with no people, plus synthetic ones. Credit the author on screen even though CC0 does not require it. Do not show the tuning images with people or children, or the shop-front image with a brand name.
- Copy model outputs from `app/tuning/results/raw.jsonl` exactly. Do not retype them from memory. The two Spanish outputs above are the recorded round 1 outputs for image 14 (variant A, then variant B, Nemotron, brief). The ID card line is variant B, Nemotron, brief.
- Same trademark rules as Round 2: crop away editor, terminal and OS branding, and use no music.
- The Round 2 video must still be recorded on the NAS. This one does not replace it.
