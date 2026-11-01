# Filled instructions (synthetic, never send)

Read this when you are unsure how a finished instruction looks after every {name} has been replaced. Everything below is synthetic. Never send these values: the album, paths, times and the language must always come from the real request and the real upstream results. The paths are shortened; real instructions carry the full real paths returned by the photo expert.

## Step 3, a since the last letter run

Values from the run: album Garden party test, photo count 12, limit 8, newest checked time from the previous letter, two paths already listed. Only the tail is shown; the rest is the step 3 instruction from SKILL.md, unchanged.

```text
(step 3 instruction unchanged) Values: album = Garden party test; album UUID or photo folder = 7f3c2a10-example; photo count = 12; limit = 8; start time = 2026-06-14 19:40:12; already listed = Photos/2026/06/IMG_2041.jpg, Photos/2026/06/IMG_2047.jpg.
```

## A name with an apostrophe

An album whose real name has a straight apostrophe, such as Dad's birthday, is written with the sign ’ in every instruction: album = Dad’s birthday. The instruction itself tells the expert that ’ stands for a straight apostrophe, and asks it to return names, paths and answer lines with ’ as well, so the values you copy from its result are already safe. If a returned value still holds a straight apostrophe, write it as ’ before you send it on. Never drop the sign or change the name in any other way.

## Step 4a, brief detail, listener language English

The parent fills max tokens with 90 and puts the brief prompt from the vision prompts reference, as one line, between Prompt begins and Prompt ends, with {language} replaced by the language from setup line 2, here English. The language never comes from place names in the results or from this example. Only the start of the prompt and the tail are shown here.

```text
(start of the step 4 instruction unchanged) max tokens 90 and this prompt, copied exactly. Prompt begins: You write the spoken description of one family photo for a listener who is blind. Step 1, privacy: ... a reason of at most 4 words in English, and nothing else. (rest of the brief prompt, with every {language} written as English) Prompt ends. (rest of the instruction unchanged) Values: photos = P1 Photos/2026/06/IMG_2101.jpg; P2 Photos/2026/06/IMG_2104.jpg; P3 Photos/2026/06/IMG_2110.jpg.
```

## Q2, a question the vision model never sees

The listener asks, in Spanish, cuál es el novio (which one is the groom). That is a person question: Q2 answers from the Family says line of the entry, or replies The photo cannot tell us that. Shall I keep the question for the family? No command is sent. A question such as what is Grandma holding only mentions a name, so it is a visible question. Where the Family says line puts Grandma on the left, Q2 step 4 writes the rewritten question what is the person on the left holding, and only that goes into the question prompt.

Note the language: it is written as a language name (Spanish), never as the phrase the listener language. In question mode it comes from the Language line of the letter.

## Steps 6 and 7, the tails only

```text
Values: folder = none; name = Listening letter - Garden party test - 2026-06-14 20-30.
```

Step 6 returned the real personal folder and no existing name, so the file name is the base name and .txt. In since mode, the folder value is the letter folder from step 2, never none.

```text
Values: folder = (real folder path from step 6); file name = Listening letter - Garden party test - 2026-06-14 20-30.txt; letter text = Dad, here are 3 new photos from Garden party test, chosen by Robin. ¶ About this letter: Taken on 14 June 2026, from 7:52 to 8:30 in the evening. ¶ How to listen: ... ¶ ¶ Photo 1 of 3. ¶ When: 14 June 2026, 7:52 in the evening. ¶ ... ¶ Photo 3: Photos/2026/06/IMG_2110.jpg
```

The whole command stays on one line. Each line break of the letter shown in chat is written as ¶ with a space on each side, and the empty line between parts as ¶ ¶. The text is the last full letter shown in chat, unchanged otherwise.

If the base name already exists, the file name is the base name, a space, a dash, a space and 2, then .txt: Listening letter - Garden party test - 2026-06-14 20-30 - 2.txt.

## Common mistakes
- Sending a phrase such as the photo list from step 3 instead of the list itself. The expert only sees the instruction.
- Leaving a {name} in the text. Stop and say which value is missing instead.
- Copying a straight apostrophe or a double quote from a family note. Write the typographic apostrophe and drop the quotes.
- Mixing the prompts: brief detail always uses the brief prompt with max tokens 90, rich detail the rich prompt with max tokens 170.
- Sending a name or a family word to the vision model in Q2.
- Using the photo folder as the letter folder. The letter folder comes only from step 2, step 6 or Q1.
