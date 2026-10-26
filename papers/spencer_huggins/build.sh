#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Rebuild the manuscript from the repository root, without tracking TeX debris.
set -eu
cd "$(dirname "$0")/../.."
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1792972800}"
export FORCE_SOURCE_DATE=1
mkdir -p build/spencer_huggins output/pdf
for pass in 1 2; do
    pdflatex -halt-on-error -interaction=nonstopmode \
      -output-directory=build/spencer_huggins \
      papers/spencer_huggins/spencer_huggins_reconstruction.tex
done
if grep -E 'Overfull|undefined references|undefined citations' \
    build/spencer_huggins/spencer_huggins_reconstruction.log; then
    echo 'Manuscript preflight failed.' >&2
    exit 1
fi
cp build/spencer_huggins/spencer_huggins_reconstruction.pdf output/pdf/
