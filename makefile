test: face.mdl main.py matrix.py mdl.py display.py draw.py gmath.py
	python main.py face.mdl
	python main.py script0.mdl
	python main.py script1.mdl
	python main.py script2.mdl
	python main.py script3.mdl
	python main.py script4.mdl
	python main.py script5.mdl
	python main.py gallery.mdl

clean:
	rm *pyc *out parsetab.py

clear:
	rm *pyc *out parsetab.py *ppm
