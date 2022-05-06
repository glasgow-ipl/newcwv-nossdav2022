#!/usr/bin/bash

mkdir archive
mkdir archive/bin
mkdir archive/figures

cp doc/paper/bin/latex-build.sh archive/bin
cp doc/paper/lib/tex/inputs/ACM-Reference-Format.bst archive
cp doc/paper/lib/tex/inputs/acmart.cls archive
cp doc/paper/papers/paper.bib archive
cp doc/paper/papers/paper.tex archive
cp doc/paper/figures/bitrate_derivative_distribution.pdf archive/figures
cp doc/paper/figures/bitrate_derivative_distribution_dynamic.pdf archive/figures
cp doc/paper/figures/cwv.pdf archive/figures
cp doc/paper/figures/new_cwv.pdf archive/figures
cp doc/paper/figures/lost_packets.pdf archive/figures
cp doc/paper/figures/lost_packets_vreno.pdf archive/figures
cp doc/paper/figures/lost_packets_newcwv.pdf archive/figures
cp doc/paper/figures/Rebuffer_Ratio.pdf archive/figures
cp doc/paper/figures/Rebuffer_Ratio_dynamic.pdf archive/figures
cp doc/paper/figures/setup.pdf archive/figures
cp doc/paper/figures/Throughput_DSL.pdf archive/figures
cp doc/paper/figures/Throughput_FTTC.pdf archive/figures

zip -r archive.zip archive
