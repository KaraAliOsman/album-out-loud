# Capability map

Read this when you need to know which expert, CLI and action serve each step, what each step changes on the NAS, and which approvals the user will see. Source: capability catalog 2.0.0 of the Uliya Skill kit 0.7.3. Action names are the likely choices of each expert; the Skill only sends plain instructions and never calls a CLI itself.

## Step by step

| Step | Expert | CLI | Likely actions | Effect | Approval |
|---|---|---|---|---|---|
| 1 find the album (regular, folder, condition or custom albums only) | photo-agent | ug-photo | `health`, `albums`, `search-hint` | read | none |
| 2 previous letter and questions (since mode) | file-agent | file-workflow, ug-filesystem | `get-user-dir`, `find`, `cat` | read | none |
| 3 choose photos and read metadata | photo-agent | ug-photo | `search-picture` (file type image, album or dir, start time, all pages), `search-screen` (screenshot category), `meta` (all paths in one call) | read | none |
| 4a to 4c describe, at most 4 photos each | photo-agent | ug-photo | `vision-vlm` (prompt, temperature, max tokens; no model value), `vision-ocr` only when words were seen | read | none |
| 5 preview and family notes | none, in chat | none | none | none | the helper says save |
| 6 letter folder and free file name | file-agent | file-workflow, ug-filesystem | `get-user-dir`, `find` | read | none |
| 7 save the letter | knowledge-agent | ug-knowledge | `save-text` (content, filename hint, path) | state change, one new file | workflow approval (catalog), form not documented |
| 8 check the saved file | file-agent | ug-filesystem | `stat`, `cat` (offset and length, start and end) | read | none |
| Q1 read one entry | file-agent | file-workflow, ug-filesystem | `get-user-dir`, `find`, `cat` | read | none |
| Q2 answer what is visible (person questions are answered from family notes and never sent) | photo-agent | ug-photo | `vision-vlm` | read | none |
| Q3 keep questions (optional) | knowledge-agent | ug-knowledge | `save-text` | state change, one new file | workflow approval (catalog), form not documented |

Main path of a letter of 6 photos (the default): 7 delegations (1, 3, 4a, 4b, 6, 7, 8), plus 1 in since mode. One chat save and one platform approval. A fast run of 4 photos needs 6 delegations. An answers-only letter needs 6 (1, 2, 3, 6, 7, 8).

The save is split on purpose: `save-text` has no action that lists folders, checks names or gives the time, so file-agent first returns the real personal folder and the names that already exist, and the Skill builds the full file name from real data before knowledge-agent saves it.

## Capabilities deliberately not used
- `create-album`, `create-album-condition`, `create-album-custom` and the other album actions: the Skill never changes the library, and each would add a workflow approval.
- `timeline`: it is a state change with workflow approval in the catalog, not a read.
- `figure-albums`, the people filters of `search-picture`, and face, baby, pet, object, location and city albums from `albums`: they are built by face, pet or object recognition, or carry the name of a child. Using them would choose photos by biometric grouping. Step 1 accepts only regular, folder, condition and custom albums, and names come only from the helper.
- `ug-document` `writing` and `translate`: gateway actions that would add prompts before the save. The letter is written directly in the listener language.
- `ug-filesystem` `echo` and `touch`: gateway writes; `save-text` returns a verified flag and the real output path instead.
- Any surveillance, music or video action.

## Things the catalog does not promise
- Whether `vision-vlm` honours temperature and max tokens, which model it uses when no model value is set, and whether that model runs on the NAS. The Skill sets no model value and states both numbers; this has to be checked on the NAS.
- The default page size and sort order of `search-picture`, and whether its start time filters by capture time or by upload time. The Skill asks the expert to page through the whole album and sort by capture time; the already listed paths guard the since mode against repeats either way.
- Whether `meta` returns place names or only coordinates, and how detailed a place name is. The Where line keeps only a city, area or venue name, and is left out when none comes back.
- Whether `save-text` keeps the file name hint exactly or adds its own ending. The Skill reports only the real output path. Step 8 reads back the folder and file name sent in step 7, and falls back to the newest file in that folder that starts with that name, so a changed ending or a straight apostrophe in the returned path does not break the check.
- The exact name of the screenshot category in Photos.
- Permissions, prerequisites and error codes, which are unknown for every action in the catalog.
- How a workflow approval appears to the user, and whether `save-text` of ug-knowledge also adds the saved file to the knowledge index of Uliya.
- Whether `vision-ocr` runs on the NAS itself and what it returns. Its text is used only to confirm the Words line of the vision model, never added to the letter.
- Whether an instruction of several KB on one line, such as the letter in step 7, reaches the expert whole, and whether the expert turns each ¶ into a line break as asked.
- How long a photo takes to describe. Nothing has been timed on a NAS.
