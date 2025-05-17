.PHONY: all tex pdf clean preview analysis reproduce figures

all: pdf

# Convert Markdown to LaTeX
tex:
	pandoc paper.md \
		--from=markdown+tex_math_dollars \
		--template=template.latex \
		--citeproc \
		-o main.tex

# Convert LaTeX to PDF using latexmk
pdf: tex
	latexmk -pdf main.tex

# Clean up auxiliary LaTeX files
clean:
	rm -f *.aux *.log *.out *.dvi *.bbl *.bcf *.blg *.run.xml *.toc
	rm -f main.tex

# Preview PDF using open (macOS)
preview: pdf
	open main.pdf

# Format for arXiv submission
arxiv-clean:
	arxiv_latex_cleaner .

# Run the Bayesian analysis
analysis:
	./run_analysis.sh

# Generate figures only
figures:
	python falls_church_model.py

# Full reproduction workflow
reproduce: analysis pdf
	@echo "Reproduction complete: Analysis run and paper generated." 