guide = {
        "a": "ah-",
        "e": "eh-",
        "i": "ee-",
        "o": "oh-",
        "u": "oo-",
        "p": "p",
        "k": "k",
        "h": "h",
        "l": "l",
        "m": "m",
        "n": "n",
        "w":"w",
        "aw":"w",
        "iw":"v",
        "ew":"v",
        "uw":"w",
        "ow":"w",
        "ai": "eye-",
        "ae": "eye-",
        "ao": "ow-",
        "ou": "ow-",
        "au":"ow-",
        "ei": "ay-",
        "iu": "ew-",
        "oi": "oy-",
        "ui": "ooey-",
        " ":" ", 
        ",":",", 
        ".":".",
        "/":"/",
        "'":"'",
        '"':'"'
    }


def validWord(word):
    characters = ["a", "e", "i", "o", "u", "p", "h", "k", "l",
                  "m", "n", "w", "'", '"', ".", ",", "/"]
    for char in word:
        if char.lower() not in characters:
            return False
        return True



def piece(word, marker):
    lst = word.split()
    for move in (2,1):
        seg = str(word[marker:marker + move]).lower()
        if seg in guide:
            return guide[seg], move
        

def pronunciate(phrase):
    
    phonetics = []
    start = 0
    
    vowels = ["a", "e", "i", "o", "u"]
    if phrase[0] in vowels:
        phonetics.append(guide[phrase[0]])
        
    while start < len(phrase):
        letters, index = piece(str(phrase), start)
        phonetics.append(letters)
        start += index
    p_word = "".join(phonetics)
    
    if "'" in p_word:
        ind = p_word.index("'")
        p_word = p_word[:ind-1] + p_word[ind:]
    
    sentence = p_word.split()
    n_sentence = []
    for word in sentence:
        word2 = word.capitalize()
        n_sentence.append(word2[:-1])
        
    p_word2 = " ".join(n_sentence)
        
    return p_word2

def createGuide(inputFile, outputFile):
    try:
        inFile = open(inputFile, 'r')
        outFile = open(outputFile, 'w')
        
        for line in inFile:
            if line[-1] == '\n':
                word = line[:-1]
            else:
                word = line
            outFile.write(pronunciate(word))
            
            if line[-1] == "\n":
                outFile.write("\n")
    
        inFile.close()
        outFile.close()

    except FileNotFoundError as error:
        print(error)

    except IOError as error:
        print(error)
