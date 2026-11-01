# Skeptic review of the tuned prompts (H2)

**Veredicto:** RESULTS.md acierta al decir que la puerta de aceptación no se cumple, pero varias cosas que da por "arregladas" no lo están. Con 40 llamadas a Nemotron (thinking off, T=0.2) encontré cuatro fallos del prompt final que su tabla no recoge, y además confirmé que repite uno que se daba por resuelto:

- **"Behind" en inglés dentro del español:** 2 de 3 rich en español con F (08, 09): *Behind hay un mar azul…*
- **Grupos de más de 5 personas enumerados uno a uno:** *un adulto con…, un adulto con…* nueve veces, unas 60-70 palabras. El límite de 25 palabras no se cumple y `checks.py` no lo mide; solo cuenta frases.
- **Preguntas de rol fuera del inglés:** F nombra al novio en alemán (0/1) y en turco (0/1), además de los 2 fallos que ya tenía en español.
- **Estatua mal contada:** *Three bronze statues of children* reaparece en brief (dos niños y un perro), igual que en E rich.

Lo que sí aguanta: la privacidad. Chat, hoja de análisis y una foto nueva CC0 de cama de hospital dan Not described 3/3. Una foto antigua de adultos en bañador en la playa no se bloquea por error (2/2). No hubo ningún corte por tokens en las 40 llamadas.

## Ediciones concretas (todo el texto de reemplazo está en inglés; todo pasa `hygiene.py`)

**1. Rich: Line 2.** Probado: 0 listas de más de 5 personas y 0 "Behind" en español en 7 salidas (R2 + R3).
Sustituir:
`The first sentence, of at most 25 words, covers all the people or things in front together, with clothing, position from left to right as seen by the viewer and visible action. The second sentence starts with Behind, said in {language}, and gives what is behind them, with plain colour names.`
por:
`The first sentence, of at most 25 words, covers the people or things in front, with clothing, position from left to right as seen by the viewer and visible action; for more than 5 people, do not list them one by one, but say a group and what most of them wear or do. The second sentence says in {language} what is behind them, with plain colour names.`
Efecto secundario: 2 de 5 salidas en español perdieron la etiqueta `Line 3:` y dejaron solo `Words: none`. El photo-agent debería aceptar una línea Words con o sin `Line 3:`.

**2. Brief y rich: género gramatical.** Insertar justo después de `never man, woman, boy, girl, he or she.` (en brief, después de `...and give their main visible action.`):
` In a language with gendered words, use the same form for every adult whatever they look like, such as un adulto in Spanish.`
- Una primera versión con *un adulto, un niño o un bebé* eliminó *una adulta* en la foto 11 (4 de 4 salidas, incluida R2 rich), pero se inventó un niño en la foto 08 dos veces de dos (*Un adulto y un niño…*).
- La redacción de arriba, sin *un niño*, se probó una sola vez (08 bien). Hay que marcarla como poco probada.
- Esto sustituye a la sugerencia de RESULTS *una persona adulta*, que nunca se probó.

**3. Question: Step 2.** Sustituir:
`if the question asks who a person is or which person is someone, uses a role or family word in any language, such as groom, bride, husband, wife, father, mother, grandmother, son or daughter, even when one person looks likely, or asks how people are related, a name, a feeling,`
por:
`if the question, in any language, asks who a person is, which person has a role or whether a person has a role, such as groom, bride, husband, wife, father, mother, grandmother, son or daughter, even when one person looks likely, or asks how people are related, a name, a gender, a feeling,`

| Pregunta | F | Edición |
|---|---|---|
| Español, novio | ya falló 2 de 2 (E, F) | UNCLEAR 1/1 |
| Alemán, Bräutigam | 0/1 | UNCLEAR 1/1 |
| Turco, damat | 0/1 | 0/1 |
| Español, padre o abuela | — | lo rechaza 2/2, pero con una frase y no con el centinela UNCLEAR |

Conclusión: el filtro de preguntas de rol en Q2, del lado del Skill, es obligatorio para cualquier idioma, no solo para el español.

**4. No adoptar:**
- Mover "In black and white" al final de Line 1: queda ambiguo (*un adulto sostiene a un bebé en blanco y negro*). Se mantiene F.
- Añadir "names printed in a corner" a la regla de Words: no tuvo efecto (*geochile* salió 3 de 3).

**Sin probar (lo marco como abierto):** que el prompt de preguntas rechace de más las preguntas de expresión visible ("is anyone smiling"). Mi prueba no sirve: en la imagen 04 no se ven caras, así que UNCLEAR era correcto.

## Ataques de revisor

- **Sobreajuste.** D, E y F se iteraron sobre las mismas imágenes que fallaban y con las que luego se puntuaron. Es un único run por celda, y F tiene 7 llamadas (brief EN n=1). Las cifras son de un conjunto de desarrollo, no un resultado de validación.
- **Sesgo del juez.** MiMo puntuó también sus propias salidas en la ronda 1. La calibración son 12 ítems etiquetados por el mismo autor de los prompts. D, E y F no los puntuó ningún juez, solo el autor. No hubo ningún evaluador ciego ni con baja visión, así que el criterio "ear" lo puntuó un modelo.
- **Modelo del NAS (Qwen3.5, unos 3B activos).** No hay ninguna evidencia sobre él.
  - Los prompts tienen entre 300 y 500 palabras, con lógica de pasos y listas de negaciones, y van dentro de un delegate que otro LLM debe copiar exactamente. Son dos puntos de fallo.
  - Si vision-vlm tiene el modo de razonamiento activo, 90 tokens dan una respuesta vacía, como ya le pasó a MiMo.
  - Hay que hacer el quick-test en el NAS antes de afirmar nada.
- **Longitud.** No hubo cortes por tokens, pero el límite de 25 palabras de rich Line 2 se incumple sin que el checker lo detecte.
- **Calidad del español (Nemotron).** Sin evaluación formal:
  - *se posa* (3 veces), cuando debería ser *posa*.
  - *letrado* en lugar de *letrero*.
  - *un adulto y un adulto* y *un niño y un niño*, en lugar de *dos adultos* y *dos niños*.
  - Etiquetas en inglés que se cuelan en el texto.
- **Cansancio y tono.** No encontré frases condescendientes.
  - Sí cansa que cada foto de un álbum antiguo empiece por "In black and white".
  - También cansa el "adult, adult, adult…", que la edición 1 resuelve para más de 5 personas.
  - En rich, una foto oscura repite lo mismo en Line 1 y Line 2.

## Afirmaciones permitidas en el PDF (en inglés, literal)

- "Tuning used cloud stand-in models (Nemotron-3.5-Super-VL, MiMo-V2.6-Pro) on 25 CC0, public-domain or synthetic images, plus 2 reviewer images; no family photo was sent anywhere. The NAS vision model itself was not tested."
- "Prompts were iterated on the same images they were scored on, one run per cell; all figures are development-set results with small samples."
- "The original prompt answered Spanish requests in English 13 times out of 16 and overran the 90-token brief budget on 7 of 25 outputs; no tuned-prompt output hit the token limit, and whole answers in the wrong language stopped, although single English words from the prompt still slipped into Spanish."
- "In every test we ran, an ID card, a chat screenshot, a lab sheet and a hospital-bed photo were withheld (Not described or UNCLEAR), and no ordinary photo, including adults in swimsuits, was wrongly withheld (small samples)."
- "Dark or blurred photos were flagged in every final-family run (10/10). Clear text was copied with at most 10% character error in every checked case."
- "English identity and role questions were declined; in Spanish, German and Turkish the prompt alone did not reliably decline them, so the Skill routes such questions to the family notes before calling the vision model."
- "An LLM judge (which also scored its own outputs) graded the first round only, agreeing with the author on 30 of 36 calibration scores; the final prompts were not judged and were not rated by blind or low-vision listeners."

**No se puede afirmar:**
- Que la puerta de aceptación se cumple.
- Que los elementos inventados (personas, figuras de estatua) están arreglados.
- Que el formato de rich está arreglado (filas 4 y 10 de la taxonomía).
- "Text fidelity 100%" en general: es 2/2 en la familia final.
- Que funciona en cualquier idioma.
- Que se escucha bien o es estable.
- Cualquier cosa sobre el rendimiento en el NAS.

## Archivos y presupuesto

- Lo que hice queda todo en `<repo>\app\tuning\`:
  - Prompts probados: `prompts\R_*.txt`, `prompts\R2_rich.txt` y `prompts\R3_rich.txt`.
  - Scripts: `review_run.py`, `make_review_prompts.py`, `make_review_prompts2.py` y `fetch_review.py`, con sus `review_jobs*.json`.
  - Salidas: `results\review_nemotron.jsonl`.
  - Imágenes nuevas: `images\26_review_hospital_bed.jpg` (CC0) y `images\27_review_bw_beach_swimsuits.jpg` (dominio público), con sus filas añadidas a `manifest.csv`. Los candidatos descargados están en `candidates_review\`.
- Los prompts finales y el paquete del Skill no se han tocado.
- Presupuesto: 40 llamadas a Nemotron, el máximo que tenía permitido. No entran en `calls_logged()`, así que el total pasa a unas 440, por encima del objetivo de unas 400.