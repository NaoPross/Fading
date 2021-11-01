TEX := xelatex
TEXARGS := -halt-on-error -interaction=nonstopmode -shell-escape=1

SOURCES := \
	Fading.tex \
	Fading.bib \
	\
	tex/docmacros.sty \
	tex/docstyle.sty \
	tex/preamble.tex \
	tex/titlepage.tex \
	\
	chapters/introduction.tex \
	chapters/theory.tex \
	chapters/implementation.tex \
	chapters/conclusions.tex \
	\
	figures/tikz/overview.tex \
	figures/tikz/psk-constellation.tex \
	figures/tikz/qam-modulator.tex \
	figures/tikz/qam-constellation.tex \
	figures/tikz/multipath-sketch.tex \
	figures/tikz/multipath-impulse-response.tex \
	figures/tikz/multipath-frequency-response-plots.tex

DATA := figures/data/multipath_frequency_response.dat

# Get the main file from the file
MAIN := $(shell sed -ne 's/^.*\!TeX root =\(.*\)$$/\1/ p' $(SOURCES))
PDF  := $(patsubst %.tex, %.pdf, $(MAIN))

ifeq ($(strip $(MAIN)),)
MAIN := $(error Failed to identify TeX root, try adding \
	`% !TeX root = <filename>` to your main tex file)
endif

.PHONY: all
all: $(PDF)

%.dat: %.py
	/usr/bin/env python3 $<

%.pdf: %.tex $(SOURCES) $(DATA)
	$(TEX) $(TEXARGS) $<
	# TODO: makeindex
	biber $(basename $(MAIN))
	$(TEX) $(TEXARGS) $<

.PHONY: clean cleanall
clean:
	@rm -vf *.aux *.aue *.lof *.log *.lot *.fls *.out *.toc *.fmt *.fot *.cb *.cb2 .*.lb *.dvi *.xdv *-converted-to.* *.bbl *.bcf *.blg *-blx.aux *-blx.bib *.run.xml *.fdb_latexmk *.synctex *.synctex\(busy\) *.synctex.gz *.synctex.gz\(busy\) *.pdfsync *.alg *.loa acs-*.bib *.thm *.nav *.pre *.snm *.vrb *.soc *.cut *.cpt *.spl *.ent *.lox *.mf *.acn *.acr *.glg *.glo *.gls *.glsdefs *.lzo *.lzs *.lol *.auxlock *.figlist
	@rm -vf tex/*.aux
	@rm -vf chapters/*.aux

cleanall: clean
	@rm -vf $(PDF)

.PHONY: continuous
continuous:
	ls $(SOURCES) | entr -d make
