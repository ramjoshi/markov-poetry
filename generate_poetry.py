import re
from sys import stdout
from sys import argv
from random import randint, choice
from collections import defaultdict

def parsePoems(poemsFile):
	poemLines = []
	with open(poemsFile) as f:

		f.readline() # first row is column header
		hasPoemStarted = False

		for line in f:
			if hasPoemStarted:
				# check for beginning of a new poem
				parts = line.split('",')
				if len(parts) >= 2:
					poemLines.append(parts[0])
					hasPoemStarted = False
				else:
					poemLines.append(line)
			else:
				# check for end of the current poem
				parts = line.split(',"')
				if len(parts) >= 2:
					poemLines.append(parts[1])
					hasPoemStarted = True
	return poemLines

def markovChain(poemLines, outputLength):
	output = []
	words = re.split(' +', " ".join(poemLines))

	transition = defaultdict(list)
	for w0, w1, w2 in zip(words[0:], words[1:], words[2:]):
		transition[w0, w1].append(w2)

	i = randint(0, len(words)-3)
	w0, w1, w2 = words[i:i+3]
	for _ in range(outputLength):
		output.append(w2)
		w0, w1, w2 = w1, w2, choice(transition[w1, w2])
	return output

def output(words):
	stdout.write(" ".join(words))

if __name__ == "__main__":
	outputLength = 500
	if len(argv) >= 2:
		outputLength = int(argv[1])

	poemLines = parsePoems("modern_renaissance_poetry.csv")
	output(markovChain(poemLines, outputLength))