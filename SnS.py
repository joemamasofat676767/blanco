from random import choices
import json

temp = 0.3
ValidChar = {"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q",
             "r","s","t","u","v","w","x","y","z"," ","."}
text = ""
text = text.lower()
text = text.split(".")

def filter(text):
    FinalText = []
    for sentance in text:
        filtered = sentance
        for letter in sentance:
            if not letter in ValidChar: filtered = filtered.replace(letter,"")
        FinalText.append(filtered)
    return FinalText
    
def CalcChance(vect, multi):
    ChanceMulti = 1 / multi
    return [abs(item ** ChanceMulti) for item in vect.values()]

class words:
    def __init__(self, word):
        self.word = word
        try:
            self.next = knowledge[0][word]
        except:
            self.next = {}
        
    def predict(self):
        next_choices = list(self.next.keys())
        if next_choices:
            return choices(next_choices, weights=CalcChance(self.next, temp))[0]
        return ""
        
try:
    with open("knowledge.json", "r") as file:
        data = json.load(file)
        knowledge = [data[0], {}]
        vocab = data[1]
        if knowledge:
            for word in knowledge[0]:
                knowledge[1][word] = words(word)
except:
    with open("knowledge.json", "w") as file:
        json.dump([{},[]], file, indent=2)
        knowledge = [{},{}]
        vocab = []
    
FirstIter = True
for sentance in filter(text):
    words_in_sentence = sentance.split()
    if not words_in_sentence:
        continue
        
    for word in words_in_sentence:
        if word not in vocab:
            knowledge[1][word] = words(word)
            vocab.append(word)
        if FirstIter:
            LastWord = word
            FirstIter = False
            continue
        if word not in knowledge[1][LastWord].next:
            knowledge[1][LastWord].next[word] = 1
        else:
            knowledge[1][LastWord].next[word] += 1
        LastWord = word
    FirstIter = True

for key in knowledge[1]:
    knowledge[0][key] = knowledge[1][key].next

predicted = "obama"
sentance = predicted + " "
finished = False
while not finished:
    if predicted in knowledge[1]:
        NextWord = knowledge[1][predicted].predict()
        if NextWord != "":
            predicted = NextWord
            sentance += predicted + " "
        else:
            finished = True
    else:
        finished = True

with open("knowledge.json", "w") as file:
    KnowledgeDump = {}
    for key in knowledge[0].keys():
        KnowledgeDump[key] = knowledge[1][key].next
    Dump = [KnowledgeDump, list(vocab)]
    json.dump(Dump, file, indent=2)
    
print(sentance)
