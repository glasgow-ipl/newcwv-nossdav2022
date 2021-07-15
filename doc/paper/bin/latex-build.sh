#!/bin/sh
# =================================================================================================
# Script to build a LaTeX document
# 
# Written by Colin Perkins
# https://csperkins.org/
#
# Copyright (C) 2003-2018 University of Glasgow
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions 
# are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# =================================================================================================

log () {
  tput setaf 2 || true
  echo $1
  tput sgr0    || true
}

separator () {
  COLS=`tput cols`
  BLANK_LINE=""

  i=0
  while [ $i -lt $COLS ]; 
  do
    BLANK_LINE="$BLANK_LINE#"
    i=`expr $i + 1`
  done

  log $BLANK_LINE
}

# =================================================================================================

if [ $# != 1 -a $# != 2 ]; then
  echo "Usage: $0 [--clean] filename.tex"
  exit 1
fi

if [ $1 = "--clean" ]; then
  MODE=clean
  shift
else
  MODE=build
fi

TEX_BASE=`basename $1 .tex`
DIR_NAME=`dirname  $1`

if [ $MODE = "clean" ]; then
  log "## Cleaning LaTeX document: $DIR_NAME/$TEX_BASE.tex"

  OUTPUTS=""
  if [ -f $DIR_NAME/$TEX_BASE.fls ]; then
    for output in `cat $DIR_NAME/$TEX_BASE.fls | sort | uniq | awk '/^OUTPUT/ {print $2}'`
    do
      OUTPUTS="$OUTPUTS $output"
    done
  fi

  for f in $OUTPUTS \
           $DIR_NAME/$TEX_BASE.bbl \
           $DIR_NAME/$TEX_BASE.blg \
           $DIR_NAME/$TEX_BASE.dep \
           $DIR_NAME/$TEX_BASE.fls \
           $DIR_NAME/$TEX_BASE.fonts
  do
    if [ -f $f ]; then
      echo "rm -f $f" && rm -f $f
    fi
  done
else
  separator
  log "## Building LaTeX document: $DIR_NAME/$TEX_BASE.tex"
  log "## "

  DID_RUN_BIBTEX=0
  SHOULD_RUN_TEX=1

  while [ $SHOULD_RUN_TEX = 1 ]; do
    SHOULD_RUN_BIB=0
    SHOULD_RUN_TEX=0

    TEXINPUTS=$DIR_NAME:
    if [ -d `pwd`/doc/paper/lib/tex/inputs ]; then
      TEXINPUTS=$TEXINPUTS:`pwd`/doc/paper/lib/tex/inputs
    fi
    TEXINPUTS=$TEXINPUTS: pdflatex -output-directory $DIR_NAME -recorder -interaction=nonstopmode -halt-on-error -file-line-error $TEX_BASE.tex
    if [ $? = 1 ]; then
      exit 1
    fi

    tput setaf 1 || true
    grep "LaTeX Warning:" $DIR_NAME/$TEX_BASE.log | sed 's/^/## /'
    grep "pdfTeX warning:" $DIR_NAME/$TEX_BASE.log | sed 's/^/## /'
    grep "Package .* Warning:" $DIR_NAME/$TEX_BASE.log | sed 's/^/## /'
    tput sgr0    || true

    # Check if we need to re-run LaTeX:
    rerun_biblatex=`grep -c 'Package biblatex Warning: Please rerun LaTeX.' $DIR_NAME/$TEX_BASE.log`
    if [ $rerun_biblatex != 0 ]; then
      log "## Need to re-run LaTeX to correct citations (biblatex)"
      SHOULD_RUN_TEX=1
    fi

    rerun_natbib=`grep -c '(natbib)                Rerun to get citations correct.' $DIR_NAME/$TEX_BASE.log`
    if [ $rerun_natbib != 0 ]; then
      log "## Need to re-run LaTeX to correct citations (natbib)"
      SHOULD_RUN_TEX=1
    fi

    rerun_labels=`grep -c 'LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right.' $DIR_NAME/$TEX_BASE.log`
    if [ $rerun_labels != 0 ]; then
      log "## Need to re-run LaTeX to correct cross-references"
      SHOULD_RUN_TEX=1
    fi

    rerun_outlines=`grep -c 'Package rerunfilecheck Warning: File .*out. has changed' $DIR_NAME/$TEX_BASE.log`
    if [ $rerun_outlines != 0 ]; then
      log "## Need to re-run LaTeX to correct outlines"
      SHOULD_RUN_TEX=1
    fi

    # Check for undefined references:
    undef_ref_count=`grep -c '.* Warning: Reference .* undefined' $DIR_NAME/$TEX_BASE.log`
    if [ $undef_ref_count != 0 ]; then
      log "## There are $undef_ref_count undefined references"
    fi

    # Check if there are undefined citations:
    undef_cite_count=`grep -c '.* Warning: Citation .* undefined' $DIR_NAME/$TEX_BASE.log`
    if [ $undef_cite_count != 0 ]; then
      log "## There are $undef_cite_count undefined citations"
      SHOULD_RUN_BIB=1
    fi

    # Check if any of the *.bib files includes have been modified since the
    # bibliography was last generated; if so, request a new run of BibTeX/Biber
    for f in `grep '\\\\bibdata{' $DIR_NAME/$TEX_BASE.aux | sed 's/\\\bibdata{//' | sed 's/}//' | sed 's/,/ /' `
    do
      if [ $DIR_NAME/$f.bib -nt $DIR_NAME/$TEX_BASE.bbl ]; then
        SHOULD_RUN_BIB=1
        log "## Need to generate bibliography: $DIR_NAME/$f.bib is newer than $DIR_NAME/$TEX_BASE.bbl"
      fi
    done

    if [ $SHOULD_RUN_BIB != 0 ]; then
      need_biber=`grep -c 'Package biblatex Warning: Please (re)run Biber' $DIR_NAME/$TEX_BASE.log`
      if [ $need_biber != 0 ]; then
        # Run Biber to generate bibliography
        separator
        (cd $DIR_NAME && biber $TEX_BASE)
        if [ $? = 1 ]; then
          exit 1
        fi
        SHOULD_RUN_TEX=1
        log "## Need to re-run LaTeX correct citations (biber)"
      elif [ $DID_RUN_BIBTEX = 0 ]; then
        # Run BibTeX to generate bibliography
        separator

        BSTINPUTS=.
        if [ -d `pwd`/lib/tex/inputs ]; then
          BSTINPUTS=$BSTINPUTS:`pwd`/lib/tex/inputs
        fi

        (cd $DIR_NAME && BSTINPUTS=$BSTINPUTS: bibtex $TEX_BASE)
        if [ $? = 1 ]; then
          exit 1
        fi
        DID_RUN_BIBTEX=1
        SHOULD_RUN_TEX=1

        tput setaf 1 || true
        grep "Warning--" $DIR_NAME/$TEX_BASE.blg | sed 's/^/## /'
        tput sgr0    || true

        log "## Need to re-run LaTeX to correct citations (bibtex)"
      fi
    fi

    separator
  done

  # Generate dependencies file for make:
  DEPENDS=""
  for dep in `cat $DIR_NAME/$TEX_BASE.fls | sort | uniq | awk '/^INPUT/ {print $2}'`
  do
    DEPENDS="$DEPENDS $dep"
  done

  for f in `grep '\\\\bibdata{' $DIR_NAME/$TEX_BASE.aux | sed 's/\\\bibdata{//' | sed 's/}//' | sed 's/,/ /' `
  do
    DEPENDS="$DEPENDS $DIR_NAME/$f.bib"
  done

  echo "$DIR_NAME/$TEX_BASE.pdf: $DEPENDS" > $DIR_NAME/$TEX_BASE.dep

  # Check the PDF metadata:
  pdfinfo  $DIR_NAME/$TEX_BASE.pdf
  echo ""

  # Check the PDF fonts:
  pdffonts $DIR_NAME/$TEX_BASE.pdf > $DIR_NAME/$TEX_BASE.fonts
  echo "Fonts:"
  cat $DIR_NAME/$TEX_BASE.fonts

  nmf=`cat $DIR_NAME/$TEX_BASE.fonts | tail -n +3 | awk '{if ($(NF-4) != "yes") print $0}' | wc -l`

  if [ $nmf -gt 0 ]; then \
    echo ""
    log "## WARNING: some fonts are not embedded"
  fi

  # Print checksums:
  echo ""
  shasum -a   1 $DIR_NAME/$TEX_BASE.pdf | awk '{print "SHA1  ", $2, $1}'
  shasum -a 256 $DIR_NAME/$TEX_BASE.pdf | awk '{print "SHA256", $2, $1}'
  echo ""

fi

# =================================================================================================
