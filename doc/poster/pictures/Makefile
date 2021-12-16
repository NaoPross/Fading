PICS := sketch.svg overview.svg

all: $(PICS)

%.pdf: %.tex
	xelatex $<

%.svg: %.pdf
	pdftocairo -svg $< $@

.PHONY: clean
clean:
	rm $(PICS) *.pdf *.log *.aux
