from random import choices

temp = 0.2
ValidChar = {"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q",
             "r","s","t","u","v","w","x","y","z"," ","."}
text = "obama love fried chicken. obama is sigma. he is good."
text = text.split(".")
vocab = set()
model = {}

def filter(text):
    FinalText = []
    for sentance in text:
        LowerSentance = sentance.lower()
        CleanSentence = "".join(letter for letter in LowerSentance if letter in ValidChar)
        FinalText.append(CleanSentence)
    return FinalText
    
def CalcChance(vect, multi):
    inv_multi = 1 / multi
    return [abs(item ** inv_multi) for item in vect]

class words:
    def __init__(self, word, next_dict=None):
        self.word = word
        self.next = {}
        
    def predict(self):
        next_choices = list(self.next.keys())
        if next_choices:
            return choices(next_choices, weights=CalcChance(self.next.values(), temp))[0]
        return ""
    
FirstIter = True
for sentance in filter(text):
    words_in_sentence = sentance.split()
    if not words_in_sentence:
        continue
        
    for word in words_in_sentence:
        if word not in vocab:
            model[word] = words(word)
            vocab.add(word)
        if FirstIter:
            LastWord = word
            FirstIter = False
            continue
        if word not in model[LastWord].next:
            model[LastWord].next[word] = 1
        else:
            model[LastWord].next[word] += 1
        LastWord = word
    FirstIter = True

predicted = "obama"
sentance = predicted + " "
finished = False

while not finished:
    if predicted in model:
        next_word = model[predicted].predict()
        if next_word != "":
            predicted = next_word
            sentance += predicted + " "
        else:
            finished = True
    else:
        finished = True

print(f"genarated: {sentance}")