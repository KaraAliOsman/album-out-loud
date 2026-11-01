# Disclosure

Read this when you need the third-party, licence or AI tool information for this Skill.

## Principal functionality built for the UGREEN Hackathon 2026
The whole Skill: the listening letter format with source labels on every line, selection rule 1, the two fixed vision prompts (brief and rich) and the question prompt, the check that keeps person questions away from the vision model, the full preview with family notes, the since the last letter record, the question mode and the questions for the family loop. All text in this package was written for this entry.

## Third-party components and open source libraries
None are bundled. The package contains only Markdown files.

## Platform and tools
- UGREEN Uliya Skill Developer Package (uliya-skill-kit 0.7.3, capability catalog 2.0.0), used for the format and the static check. Source: UGREEN Hackathon starter kit. Licence: the kit ships no licence file; its use is subject to the developer tools license agreement referenced in the official rules. No kit file is included.
- At run time the Skill delegates to the built-in Uliya experts, which use whichever models the user has set for Uliya. It sets no model value of its own.

## Data flows at run time
- Photos are sent only to the vision-vlm and vision-ocr actions of the NAS photo expert, with no model value set; whether that model runs on the NAS itself has not been verified.
- The conversation text, including family notes, questions and descriptions, is handled by whichever model the user has set for Uliya.
- The Skill reads the chosen album and its photo details, searches file names in the personal folder and its subfolders for earlier letters of that album, and reads those letters and their Listener questions files. It writes only the letter and questions files the helper approves, in the personal folder of the user or the folder of the earlier letter.

## Guidance that informed the writing (paraphrased, nothing copied)
- Image description guidance from the W3C WAI images tutorial, the NCAM and DIAGRAM Center image description guidelines, and the Cooper Hewitt guidelines for image description.
- Research on describing people in automated alt text (Hanley and others, AIES 2021).
- Public Agent Skills examples from Anthropic (Apache-2.0), for structure only.

## AI tools used to build the Skill
- Claude Code (Anthropic): drafting and reviewing the Markdown, checking it against the rules of the developer package, and building and running the prompt-tuning and dry-run scripts. The entrant directed the work and reviews and edits all text before submission.
- Prompt tuning only: tuning used cloud stand-in models (Nemotron-3.5-Super-VL, MiMo-V2.6-Pro, through the Primalabs API) on 25 CC0, public-domain or synthetic images, plus 2 openly licensed reviewer images; no private or personal photo was sent anywhere. MiMo-V2.6-Pro also graded round 1 outputs as an LLM judge. The NAS vision model itself was not tested. Prompts were iterated on the same images they were scored on, one run per cell; all figures are development-set results with small samples. At run time the Skill asks the photo expert to use only the vision-vlm action of the NAS.
- Dry run only: Nemotron-3.5-Super-VL also played the Uliya parent agent, reading this package, against expert results written by hand. No NAS, no real expert and no real photo library were involved.

## Test data
No test images are included in this package, and it holds no real personal data.

## Licence of this package
The text of this package is the original work of the entrant, submitted under the hackathon rules. UGREEN receives the licence described in the official rules. No other licence is granted with this submission.
