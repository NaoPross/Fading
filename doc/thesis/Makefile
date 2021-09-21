TEX := pdflatex 
TEXARGS := -halt-on-error -interaction=nonstopmode

SOURCES := Fading.tex tex/classicthesis.sty tex/classicthesis-config.tex

# Get the main file from the file
MAIN := $(shell sed -ne 's/^.*\!TeX root =\(.*\)$$/\1/ p' $(SOURCES))
PDF  := $(patsubst %.tex, %.pdf, $(MAIN))

ifeq ($(strip $(MAIN)),)
MAIN := $(error Failed to identify TeX root, try adding \
	`% !TeX root = <filename>` to your main tex file)
endif

.PHONY: all
all: $(PDF)

%.pdf: %.tex $(SOURCES)
	$(TEX) $(TEXARGS) $<

.PHONY: clean cleanall
clean:
	@rm -vf *.aux *.aue *.lof *.log *.lot *.fls *.out *.toc *.fmt *.fot *.cb *.cb2 .*.lb *.dvi *.xdv *-converted-to.* *.bbl *.bcf *.blg *-blx.aux *-blx.bib *.run.xml *.fdb_latexmk *.synctex *.synctex\(busy\) *.synctex.gz *.synctex.gz\(busy\) *.pdfsync *.alg *.loa acs-*.bib *.thm *.nav *.pre *.snm *.vrb *.soc *.cut *.cpt *.spl *.ent *.lox *.mf *.acn *.acr *.glg *.glo *.gls *.glsdefs *.lzo *.lzs

cleanall: clean
	@rm -vf $(PDF)
