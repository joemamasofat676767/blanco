from random import choices, choice, uniform
from pathlib import Path
import flooride as fd
import time
import json

ROOT = Path(__file__).parent.parent
KNOWLEDGE_PATH = str(ROOT/"main"/"knowledge.flrd")
TRAIN_PATH = ROOT/"main"/"train.txt"

TEMP = 0.3
CHANCE_MULTI = 1 / TEMP
LR = 0.1
VALID_CHAR = {"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q",
				"r","s","t","u","v","w","x","y","z"," ","."}

with open(TRAIN_PATH, "r") as file:
	text = file.read()
text = text.lower()
text = text.split(".")

def filter(text):
	FinalText = []
	for sentence in text:
		filtered = sentence
		for letter in sentence:
			if letter not in VALID_CHAR:
				filtered = filtered.replace(letter, "")
		FinalText.append(filtered)
	return FinalText

def GenRef(tokens):
	return [sum([knowledge[token].GetNext()[i] for token in tokens if token in knowledge]) / len(tokens) for i in range(3)]

def CalcChance(vect):
	return [abs(item ** CHANCE_MULTI) for item in vect]
   
def generate(StartText, ref=None):
	predicted = StartText
	sentance = predicted + " "
	finished = False
	while not finished:
		if predicted in knowledge:
			if not ref:
				NextWord = predict(predicted)
			else:
				differences = [(word, taylor(knowledge[word.decode()].GetEmbeddings(), ref)) for word in knowledge[predicted].GetNext()]
				if differences:
					SortedDifferences = sorted(differences, key=lambda word: word[1])
				else:
					finished = True
					break
				NextWord = choice(SortedDifferences[:len(SortedDifferences) // 3 + 1])[0].decode()
			if NextWord != "":
				predicted = NextWord
				sentance += predicted + " "
			else:
				finished = True
		else:
			finished = True
	return sentance[:-1] + "."

def taylor(embedding1, embedding2):
	child =  sum(embedding1[i] * embedding2[i] for i in range(len(embedding1)))
	parent =  sum(embedding1[i] ** 2 for i in range(len(embedding1))) ** 0.5 * sum(embedding2[i] ** 2 for i in range(len(embedding1))) ** 0.5
	a = child / (parent + 0.01)
	theta = round(1.570796 - a - (a ** 3 / 6) - (3 * a ** 5 / 40), 4)
	return 90 / (theta + 0.01)

def predict(word1):
	NextChoices = knowledge[word1].GetNext()
	if NextChoices:
		difference = [taylor(knowledge[word1].GetEmbeddings(), knowledge[word2].GetEmbeddings()) for word2 in knowledge[word1].GetNext()]
		return choices(NextChoices, weights=CalcChance(difference))[0]
	return ""

fd.mat.lay(KNOWLEDGE_PATH)
mats = fd.mat.GetMats()

knowledge = {}
for mat in mats:
	knowledge[mat.GetWord().decode()] = mat

print(knowledge)

if __name__ == "__main__":
	while True:
		epoch = input("epoches: ") 
		if epoch.isdecimal():
			epoch = int(epoch)
			break
		else:
			print("enter num")
	start = time.perf_counter()
	for i in range(epoch):
		FirstIter = True
		for sentance in filter(text):
			WordsInSentence = sentance.split()
			if not WordsInSentence:
				continue     
			for word in WordsInSentence:
				if word not in knowledge:
					knowledge[word] = fd.mat.MakeMat(word.encode("utf-8"), [], [round(uniform(-2,2), 3) for _ in range(3)])
				if FirstIter:
					LastWord = word
					FirstIter = False
					continue
				if word not in knowledge[LastWord].GetNext():
					knowledge[LastWord].sow(word)
				for i in range(fd.mat.inspect()[0]):
					knowledge[LastWord].restyle("e", str(knowledge[LastWord].GetEmbeddings()[i] + round((knowledge[word].GetEmbeddings()[i] - knowledge[LastWord].GetEmbeddings()[i]) * LR, 3)), i)
					mag = sum([knowledge[LastWord].GetEmbeddings()[i] ** 2 for i in range(3)]) ** 0.5
					knowledge[LastWord].restyle("e", str(round(knowledge[LastWord].GetEmbeddings()[i] / mag, 3)), i)
				LastWord = word
			FirstIter = True
		print(f"finished {i+1} epoch")
	end = time.perf_counter()
	
	TimeTook = (end - start) * 1000
	print(f"| trained: {epoch} epochs | took: {TimeTook:.3f}ms |")
	
	running = True
	while running:
		prompt = [token for token in filter(input("you: ").split(".")) if token != ""]
		if prompt:
			start = time.perf_counter()
			response = generate("the", GenRef(prompt))
			end = time.perf_counter()
			print(f"blanc(thought for: {(end-start)*1000:.3f}ms): {response}")
		else:
			print("enter something")
	
	fd.mat.lay(KNOWLEDGE_PATH)
