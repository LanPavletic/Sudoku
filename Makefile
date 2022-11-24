run:
	python3 sudoku/game.py

setup: requirements.txt
	pip install -r requirements.txt

clean:
	rm -rf sudoku/__pycache__
