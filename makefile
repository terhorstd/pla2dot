
Usecase-109.png:

%.svg: %.dot
	dot -Tsvg $< >$@

%.png: %.dot
	dot -Tpng $< >$@

%.dot: %.data
	./pla2dot.py $< $@
