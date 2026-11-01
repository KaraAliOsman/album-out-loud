# Quick test for reviewers

Read this when you test the Skill on a NAS with no prepared data, or check that requests reach this Skill.

## Before you start (not timed)
- The Uliya vision model of the NAS is installed and switched on.
- Indexing of the new photos has finished before each case. The Skill needs the screenshot category of Photos to leave screenshots out; it uses no people, face or baby albums, so face grouping can stay off.

## Seed data (about 15 minutes)
1. Set a small party table: for example a cake or cupcakes, cups, a garland, a greeting card with printed words and a guest book with a printed cover. No people are needed.
2. With a phone, take 12 photos of the table from different sides, about one per minute over 12 minutes, so that no two chosen photos share a minute. At least two must show printed words. Phone photos carry real camera times.
3. Hold back the 2 newest photos for Case 2; make the last one the guest book cover.
4. Upload the other 10 to the Photos library and wait until they appear in the Photos timeline.
5. Put them in an album named Garden party test. If creating an album is not convenient, upload them into a new folder named Garden party test instead; the Skill accepts a photo folder.

## Case 1: first letter (fast run of 4 photos; estimated 5 to 7 minutes, not yet timed)
Say: Album Out Loud, make a listening letter for Dad from the album Garden party test, 4 photos.
Expected:
- One setup message with the defaults filled in; reply go.
- 4 photos chosen across the 10 minutes, including the oldest and the newest, described in one group.
- A preview that starts with Preview: 4 of 10 photos chosen, then the full letter, from the opening line to the photo files. Type 2: the cups from the holiday. The full letter comes back with that note. Say save.
- A platform approval may follow the chat save; the catalog marks save-text with a workflow approval, but how it appears has not been seen yet. After it, the reply shows the real file path and the size.

The full run with the default of 6 photos is estimated at 7 to 10 minutes; nothing has been timed on a NAS yet.

## Case 2: since the last letter
Upload the 2 photos held back and wait for indexing. Say: Album Out Loud, photos since the last letter for Dad, album Garden party test.
Expected: only the 2 new photos are described. Photos that were left out of letter 1 do not come back, because they are older than its Newest photo checked line. The preview says that photos added later but taken earlier are not in since letters.

## Case 3: question about one photo
The guest book cover is in letter 2, the latest letter. Find its photo number, then say: Album Out Loud, photo N of the Garden party test letter, what words are on the book cover? (with that number for N)
Expected: a reply that starts with In the Garden party test letter of, the date of letter 2 and the photo, then AI guess, may be wrong, in at most 2 sentences.
Then ask: who gave Dad this book?
Expected: The photo cannot tell us that. Shall I keep the question for the family? Say yes; the kept line is shown. Say save now; one more approval saves the questions file.
Optional: ask which person is Dad in a photo with people and no Family says line. Expected: the same reply, with no vision step before it.

## Case 4: answers-only letter
Say: Album Out Loud, photos since the last letter for Dad, album Garden party test.
Expected: no new photos, and an answers-only preview that lists the kept question. Type A1: a gift from the neighbours. Say save and approve.

## Pass checklist
- The reply shows a real output path, and the file name starts with Listening letter - Garden party test -.
- The file starts with the opening line, Dad, here are 4 photos from Garden party test, and contains Photo 1 of 4.
- No line says none, and words that text recognition did not confirm are labelled Words in the photo, AI reading.
- No AI guess line contains a name or a gender word.
- For the helper: photo files is the last section, has the Language line, and ends with real paths.
- Approvals seen: one per letter, plus one only when questions are kept.
- Optional, needs extra setup: a photo of a baby or child in a bath stays Not described. This privacy item was never tested.
- Optional: open the file with NVDA, VoiceOver or TalkBack in any plain text app, check that no signs are read out, and use find to jump to Photo 3.

## Edge cases
- An album name that does not exist: no results with search suggestions, and nothing is saved.
- Deny the approval dialog at the save: nothing is saved and the full letter is shown in chat.
- Optional, needs extra setup: an album with only videos gives no results for still photos.

## Routing checks (say each one, see whether this Skill answers)
Should reach Album Out Loud:
- my dad lost his sight last year, can his screen reader go through the Garden party test album
- describe the beach photos for my sister, she is blind
- anything new in Garden party test since the last letter for Dad?
- Dad asks what is on the table in photo 2 of the garden party letter
- my aunt has low vision, can she hear what is in the birthday album
- Album Out Loud for my uncle, folder Garden party test

Should not reach it:
- make a new album with all the photos from June
- find the blurry photos in Garden party test
- write social media captions for these photos
- read this bank letter PDF aloud
- who is this person in my photo (no letter involved)
- summarize my notes on low vision aids
