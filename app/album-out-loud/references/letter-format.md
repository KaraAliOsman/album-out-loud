# Listening letter format

Read this when you build the letter in step 5, or answer a question in Q2. It holds the wording of every part, the rule for each line, the answers-only letter, the reasons, and a full synthetic example. The preview notices are in step 5 of SKILL.md.

## Parts and wording
- Plain text: no hash marks, tables, bold, links or emoji. An empty line separates the parts. Use the typographic apostrophe only.
- Order: opening line, About this letter, How to listen, one entry per photo, Answers from the family (only when there are answers), What this letter cannot tell you (only when it has content), closing line, For the helper: photo files.
- Language: everything the listener hears, labels and dates included, is in the listener language. In Spanish, for example: Foto 1 de 3., Cuándo, Dónde, La familia dice, Suposición de la IA, Palabras en la foto, Palabras en la foto, lectura de la IA, Sobre esta carta, Cómo escuchar, Respuestas de la familia, Lo que esta carta no puede decirte. The For the helper: photo files part stays in English in every language, because later runs read it back.
- Opening line: {listener}, here are {M} photos from {album name}, chosen by {helper}. When the listener is the default your relative, start with Here are. A since letter says {M} new photos.
- About this letter: one sentence, Taken on {date}, from {first time} to {last time}, or Taken between {first date} and {last date} when the dates differ. If every described photo is an old print or in black and white, add: Every photo is an old print or in black and white.
- How to listen: Each photo starts with its number, such as Photo 1 of {M}. Lines that start with Family says are from {helper}, and names come only from them. Lines that start with AI guess were written by a computer and may be wrong.
- What this letter cannot tell you: one short sentence per photo that was not described, such as Photo 3 was not described, and one per open question, in the second person, such as Your question about photo 2 of the earlier letter, who gave you the guest book, is still with the family. An answered question is not listed. Left out when there is nothing to list.
- Closing line: From {helper}. The rest of this letter is a file list for the helper; you can stop listening here.
- For the helper: photo files: the line Keep this part for the next letter. It holds folder names, so remove it from any copy shared outside the family. Then the line Language: {language}, the line Selection rule: 1, the line Newest photo checked: {newest checked time from step 3, or unknown}, one line Open question: {question line} per open question left unanswered, then one line Photo N: {real path} per photo, with the full real path exactly as step 3 returned it.

## Rules for each entry line
- Each entry starts with the line Photo N of M., then these lines in this order, each only when it has content: When, Where, Family says, AI guess, Words in the photo.
- When: the date and time from step 3, as people say them in the listener language: 14 June 2026, 7:52 in the evening, or 20 de julio de 2026, 1:42 de la tarde. Hours 0 to 11 are in the morning (0 is 12), 12 stays 12 and is in the afternoon, 13 to 17 minus 12 are in the afternoon, 18 to 23 minus 12 are in the evening; 11:20 is 11:20 in the morning. Never add a weekday. If step 3 said file, write When: 14 June 2026, from the file date, may be wrong. If the AI guess starts with In black and white or An old print, or the same words in the listener language, or that start was dropped because every photo has it, write When: copied or scanned on 14 June 2026; the photo itself may be older.
- Where: only a city, area or venue name the library gave. Never a street address or coordinates. No Where line when there is none.
- Family says: the note of the helper in their own words, with only the cleanup of check rule 6 in SKILL.md.
- AI guess: Line 1, plus Line 2 in rich mode. Copy the model words. Drop a lead-in such as this photo shows and drop any name, without adding words. Never add a confidence number. In rich mode with more than 8 photos, keep only Line 1. When every described photo starts with In black and white or An old print, drop those words from each AI guess and start with the next word.
- Words in the photo, only when the vision model gave a Words line other than none:
  - Every word of the Words line is also in the vision-ocr result, ignoring case: Words in the photo: and the Words line words.
  - Otherwise: Words in the photo, AI reading: and the Words line words.
  - Never add other text from vision-ocr. Leave out numbers of 5 or more digits, number plates, phone numbers and addresses, even when they are split by spaces or dashes. At most 25 words, then and more text. Never translate.
- Not described: keep the Photo N of M. line and the When line, then write This photo was not described. Reason: and the reason returned.
- Answers from the family, one line per answer: From an earlier letter, photo {photo number}: you asked {question, in the second person}. {helper, with a capital first letter} says: {answer}.

## Answers-only letter
In since mode, when step 3 finds no new photos but step 2 returned open questions: no step 4. The opening line is {listener}, here are the family answers to your questions about {album name}, from {helper}. Then About this letter (no new photos since the last letter), How to listen, Answers from the family, What this letter cannot tell you (questions still open), the closing line, and For the helper: photo files with the previous Newest photo checked line and any questions still open. Then the normal preview, save and check follow.

## Why the format looks like this
- The letter is plain text with no hash marks or other markup, so a screen reader never reads out signs, and the same file works in any text app, on a phone, in large print, or read aloud by the helper. Every entry starts with the line Photo N of M., so the listener can find Photo 3 to jump to it, and always knows how many photos are left.
- It opens with the name of the listener and closes with the name of the helper, because it is a letter from someone, not a report.
- One fact per line, and each line starts with its source label. The listener can stop after When and Family says, or listen on to the AI guess. Words read only by the vision model carry AI reading in the label, before the words, so the listener hears the source first.
- Family knowledge comes before the AI guess, and the AI guess comes before the words in the photo, so the listener knows what the photo is before hearing any text from it. The AI guess never contains a name, and the label itself carries the hedge, so the guess needs no extra hedging words. Possibly appears at most once and confidence numbers never appear.
- A line with no content is left out. The listener never hears none.
- Dates are written out in full and without a weekday, because a wrong weekday read aloud is a fact the listener cannot check. Times are written as people say them, because 19:52 read aloud next to a date can sound like a year.
- When the camera time is missing and only the file date exists, the When line says so. An old print or a black and white photo usually carries the date it was scanned or copied, so the When line says that and leaves the real date to the family.
- When every photo is an old print, About this letter says it once, so the listener does not hear the same words at the start of every guess.
- Where holds only a city, area or venue name, never a street or house number, because the helper may share the file.
- Words in the photo come only from the Words line of the vision model, whose prompt already leaves out small print, logos and number plates. Text recognition only confirms those words; it can read every scrap of background text, so its extra text is never added. Long numbers, plates, phones and addresses are left out because the file may be shared.
- What this letter cannot tell you lists only what this letter is missing: photos that were not described and questions still with the family.
- The photo files section is for the helper, not the listener. It sits last, the closing line tells the listener they can stop there, and it holds the lines that the next letter and question mode read back: Language, Selection rule, Newest photo checked, Open question and one Photo N: line per photo. It holds full NAS paths, which can include account and folder names, so its first line tells the helper to remove it before sharing the letter outside the family. A ’ in a path there stands for a straight apostrophe in the real file name.

## File names
- Letter: Listening letter - {album} - {newest photo checked, as year-month-day hour-minute}.txt, or Listening letter - {album} - {date} - 2.txt, then - 3.txt, when that name exists. The date is the time of the newest photo checked, not the save date, so the name never depends on a clock and later letters sort after earlier ones. A listener who asks about an older letter can name the date of its photos.
- Questions: Listener questions - {name of the latest letter without .txt} - {number}.txt, in the same folder as the letter.
- Slashes, backslashes and colons in the album name become dashes.

## Selection rule 1
Still photos only, without videos and screenshots, sorted by capture time across the whole album. Photos already listed in an earlier letter and photos older than its Newest photo checked line are left out. When more photos remain than the limit, the oldest and the newest are always kept and the rest are spread evenly by position in capture order. If a pick falls in the same minute as the photo chosen before it, the next photo in a later minute takes its place, while one remains. The rule number is written into each letter so that a later letter can explain what it chose.

Photos added to the album later but taken before Newest photo checked do not appear in since letters; the preview says so, and a new letter includes them. The preview also says how many photos qualified and how many were chosen.

## Full example (synthetic data, a second letter for the same album)

```text
Dad, here are 3 new photos from Garden party test, chosen by Robin.
About this letter: Taken on 14 June 2026, from 7:52 to 8:30 in the evening.
How to listen: Each photo starts with its number, such as Photo 1 of 3. Lines that start with Family says are from Robin, and names come only from them. Lines that start with AI guess were written by a computer and may be wrong.

Photo 1 of 3.
When: 14 June 2026, 7:52 in the evening.
Where: Riverside Park.
Family says: the lanterns Sam brought back from the trip.
AI guess: A row of paper lanterns glows above a long table at dusk.

Photo 2 of 3.
When: 14 June 2026, from the file date, may be wrong.
Family says: the cake, lemon with blueberries.
AI guess: Three adults and a child stand around a round cake with candles.
Words in the photo, AI reading: HAPPY SUMMER.

Photo 3 of 3.
When: 14 June 2026, 8:30 in the evening.
This photo was not described. Reason: private paper.

Answers from the family:
From an earlier letter, photo 4: you asked who gave you the guest book. Robin says: the neighbours, for your birthday.

What this letter cannot tell you: Photo 3 was not described.

From Robin. The rest of this letter is a file list for the helper; you can stop listening here.

For the helper: photo files
Keep this part for the next letter. It holds folder names, so remove it from any copy shared outside the family.
Language: English
Selection rule: 1
Newest photo checked: 2026-06-14 20:30:41
Photo 1: Photos/2026/06/IMG_2101.jpg
Photo 2: Photos/2026/06/IMG_2104.jpg
Photo 3: Photos/2026/06/IMG_2110.jpg
```

The example paths are shortened. A real letter keeps the full real path exactly as the photo expert returned it.

## Question mode replies
Each reply starts with the letter and the photo in spoken form, for example In the Garden party test letter of 14 June 2026, photo 2. The exact file name is used only in the questions file. Then one of:
- From the family notes: the cake was lemon with blueberries.
- From the letter: it was taken on 14 June 2026, at 8:30 in the evening.
- AI guess, may be wrong: there are three candles on the cake. They stand in the middle, next to a small flag.
- The photo cannot tell us that. Shall I keep the question for the family?

From the family notes is used for person questions (who someone is, which one, whether someone is a role or relation such as groom or grandmother, gender, age or feelings), answered only from a Family says line; these questions never go to the vision model. A question that only mentions a name, such as what is Grandma holding, is a visible question, sent with the name replaced by a position. From the letter is used for when and where questions, answered from the When and Where lines, which come from the camera and the library. AI guess is used for what is visible. The last line is used when the vision model answers UNCLEAR, when a visible question is about a photo that was not described, or when a person question has no answer in the Family says line. A photo that was not described is never sent to the vision model in question mode.

## Questions file
One line per kept question:

```text
Photo 4, Listening letter - Garden party test - 2026-06-14 19-40, who gave Dad the guest book, asked by Dad.
```
