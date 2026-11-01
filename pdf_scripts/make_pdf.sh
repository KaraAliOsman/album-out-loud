#!/usr/bin/env bash
# Rebuilds the accessible (tagged) Round 1 PDF from submission/pdf_source.md. Run from the project root.
set -e
python -I pdf_scripts/count_words.py submission/pdf_source.md --write
uv run --quiet --with markdown python -I pdf_scripts/build_tagged.py submission/pdf_source.md pdf_scripts/flow.png pdf_scripts/tagged/proposal.html
EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
WIN="$(cygpath -w "$PWD")"
URL="file:///$(cygpath -m "$PWD")/pdf_scripts/tagged/proposal.html"
"$EDGE" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="$WIN\pdf_scripts\tagged\proposal.pdf" "$URL" 2>/dev/null
# Edge can return before the PDF is written: wait until it is newer than the HTML, then let it settle.
for i in $(seq 1 30); do [ pdf_scripts/tagged/proposal.pdf -nt pdf_scripts/tagged/proposal.html ] && break; sleep 1; done; sleep 2
cp pdf_scripts/tagged/proposal.pdf submission/AlbumOutLoud_Round1_Proposal.pdf
python -I pdf_scripts/count_words.py submission/pdf_source.md
