# Лучше бы это переделать с latexmk
BUILD = xelatex -halt-on-error -interaction=nonstopmode -shell-escape -output-directory=build main
all: build
	$(BUILD) && biber build/main && $(BUILD) && $(BUILD) && mv build/main.pdf ./ || >&2 echo "Error while building a PDF"
fast: build
	$(BUILD) && mv build/main.pdf ./
build:
	mkdir build
clean:
	rm -rf build

ncw:
	test -s main.tex && { echo "main.tex exist! Exiting..."; exit 1; } || echo "Copying files"
	cp -r templates/images .
	cp templates/course/* .
	mv course.tex main.tex
	mv title-course.tex title.tex
