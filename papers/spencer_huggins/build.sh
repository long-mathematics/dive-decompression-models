#!/bin/sh
# Reproducible local build; requires a standard TeX Live pdflatex installation.
set -eu
cd "$(dirname "$0")/../.."
mkdir -p output/pdf
pdflatex -halt-on-error -interaction=nonstopmode -output-directory=output/pdf papers/spencer_huggins/spencer_huggins_reconstruction.tex
pdflatex -halt-on-error -interaction=nonstopmode -output-directory=output/pdf papers/spencer_huggins/spencer_huggins_reconstruction.tex
