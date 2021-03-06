TEX := xelatex
TEXARGS := --halt-on-error --interaction=nonstopmode --shell-escape=1 --enable-write18

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
	figures/tikz/multipath-frequency-response-plots.tex \
	figures/tikz/tapped-delay-line.tex \
	figures/tikz/ring-of-scattering-objects.tex \
	figures/tikz/rayleigh-rice-pdf-plots.tex \
	figures/tikz/packet-frame.tex \
	figures/tikz/qpsk-simulations-static.tex \
	figures/tikz/qpsk-simulations-dynamic.tex \
	figures/tikz/qam-simulations-dynamic.tex \
	figures/tikz/hardware.tex

DATA := \
	figures/data/multipath_frequency_response.dat \
	figures/data/rice_pdf.dat \
	\
	figures/data/qpsk_hw_lab.dat \
	figures/data/qpsk_hw_outdoors_1.dat \
	figures/data/qam_hw_lab.dat \
	\
	figures/data/qpsk_sim_nochannel.dat \
	\
	figures/data/qpsk_sim_static_firblock_los_halfsymb.dat \
	figures/data/qpsk_sim_static_firblock_nlos_halfsymb.dat \
	figures/data/qpsk_sim_static_firblock_los_vec.dat \
	figures/data/qpsk_sim_static_firblock_nlos_vec.dat \
	\
	figures/data/qpsk_sim_dynamic_grblock_los_etsi_doppler5_k5.dat \
	figures/data/qpsk_sim_dynamic_grblock_los_etsi_doppler70_k5.dat \
	figures/data/qpsk_sim_dynamic_grblock_nlos_etsi_doppler5.dat \
	figures/data/qpsk_sim_dynamic_grblock_nlos_etsi_doppler70.dat \
	\
	figures/data/qam_sim_dynamic_grblock_los_etsi_doppler5_k5.dat \
	figures/data/qam_sim_dynamic_grblock_los_etsi_doppler70_k5.dat \
	figures/data/qam_sim_dynamic_grblock_nlos_etsi_doppler5.dat \
	figures/data/qam_sim_dynamic_grblock_nlos_etsi_doppler70.dat


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
	mkdir -p figures/externalized
	$(TEX) $(TEXARGS) $<
	# bibliography
	biber $(basename $(MAIN))
	$(TEX) $(TEXARGS) $<
	# embed fonts
	# gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dEmbedAllFonts=true -sOutputFile=$@_font_embedded.pdf -f $@

.PHONY: clean cleanall
clean:
	@rm -vf *.aux *.aue *.lof *.log *.lot *.fls *.out *.toc *.fmt *.fot *.cb *.cb2 .*.lb *.dvi *.xdv *-converted-to.* *.bbl *.bcf *.blg *-blx.aux *-blx.bib *.run.xml *.fdb_latexmk *.synctex *.synctex\(busy\) *.synctex.gz *.synctex.gz\(busy\) *.pdfsync *.alg *.loa acs-*.bib *.thm *.nav *.pre *.snm *.vrb *.soc *.cut *.cpt *.spl *.ent *.lox *.mf *.acn *.acr *.glg *.glo *.gls *.glsdefs *.lzo *.lzs *.lol *.auxlock *.figlist
	@rm -vf tex/*.aux
	@rm -vf chapters/*.aux
	@rm -vf figures/tikz/*.aux
	@rm -vfrd figures/externalized

cleanall: clean
	@rm -vf $(PDF)

.PHONY: continuous
continuous:
	ls $(SOURCES) | entr -d make
