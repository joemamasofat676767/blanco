from random import choices, uniform
from pathlib import Path
import json

KNOWLEDGE_PATH = Path(__file__).parent.parent/"main"/"knowledge.json"

TEMP = 0.3
VALID_CHAR = {"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q",
				"r","s","t","u","v","w","x","y","z"," ","."}
text = ""
text = text.lower()
text = text.split(".")

def filter(text):
	FinalText = []
	for sentance in text:
		filtered = sentance
		for letter in sentance:
				if not letter in VALID_CHAR: 
					filtered = filtered.replace(letter,"")
		FinalText.append(filtered)
	return FinalText
    
def CalcChance(vect, multi):
	ChanceMulti = 1 / multi
	return [abs(item ** ChanceMulti) for item in vect]
    
def generate(StartText):
	predicted = StartText
	sentance = predicted + " "
	finished = False
	while not finished:
		if predicted in knowledge:
			NextWord = knowledge[predicted].predict()
			if NextWord != "":
				predicted = NextWord
				sentance += predicted + " "
			else:
				finished = True
		else:
			finished = True
	
	return sentance

class words:
	def __init__(self, word, embedding=[0,0,0]):
		self.word = word
		try:
			self.next = knowledge[word][0]
		except:
			self.next = []
		self.embedding = embedding

	def predict(self):
		NextChoices = list(self.next)
		if NextChoices:
			difference = []
			for word in self.next:
				child =  sum(self.embedding[i] * knowledge[word].embedding[i] for i in range(len(self.embedding)))
				parent =  sum(self.embedding[i] ** 2 for i in range(len(self.embedding))) ** 0.5 * sum(knowledge[word].embedding[i] ** 2 for i in range(len(self.embedding))) ** 0.5
				a = child / (parent + 1)
				theta = round(1.570796 - a - (a ** 3 / 6) - (3 * a ** 5 / 40), 4)
				diff = 90 / (theta + 1)
				difference.append(diff)
			return choices(NextChoices, weights=CalcChance(difference, TEMP))[0]
		return ""
  
try:
	with open(KNOWLEDGE_PATH, "r") as file:
		knowledge = json.load(file)
		if knowledge:
			for word in knowledge:
				knowledge[word] = words(word,knowledge[word][1])
except:
	with open(KNOWLEDGE_PATH, "w") as file:
		json.dump({}, file, indent=2)
		knowledge = {}

print(knowledge)

if __name__ == "__main__":
	FirstIter = True
	for sentance in filter(text):
		WordsInSentence = sentance.split()
		if not WordsInSentence:
			continue
        
		for word in WordsInSentence:
			if word not in knowledge:
				knowledge[word] = words(word, [round(uniform(-1,1), 3) for _ in range(3)])
			if FirstIter:
				LastWord = word
				FirstIter = False
				continue
			if word not in knowledge[LastWord].next:
				knowledge[LastWord].next.append(word)
			LastWord = word
		FirstIter = True
		
	print(generate("obama"))
	
	with open(KNOWLEDGE_PATH, "w") as file:
		KnowledgeDump = {}
		for key in knowledge.keys():
			KnowledgeDump[key] = knowledge[key].next, knowledge[key].embedding
		Dump = KnowledgeDump
		json.dump(Dump, file, indent=2)
