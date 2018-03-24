import pickle
import re

#functions for adding names
def addName(name):
    global listOfNames
    #remove <> tags
    test = re.search('>(.*)<', str(name))
    if test:
        name = test.group(1)
        listOfNames.append(name)
    else:
        #remove . and beginning/ending whitespace
        if name[0] == ' ':
            name = name[1:]
        if name[len(name)-1] == ' ' or name[len(name)-1] == '.':
            name = name[:len(name)-1]
        #check if actual name
        if re.search('with ', str(name)) or re.search('the ', str(name)) or re.search('freinds', str(name)) or re.search('Director',str(name)) or re.search('of ',str(name)) or re.search('of<',str(name)) or re.search('officer',str(name))or re.search('-chair',str(name)) or re.search('\(',str(name)):
            return
        else:
            #finally check if in list already and if not add
            if name.find('\\') != -1:
                name = name[:name.find('\\')]
            if name not in listOfNames:
                listOfNames.append(name)
def addLargeName(name):
    global listOfNames
    #remove <> tags
    test = re.search('>(.*)<', str(name))
    if test:
        name = test.group(1)
        listOfNames.append(name)
    else:
        #remove . and beginning/ending whitespace
        if name[0] == ' ':
            name = name[1:]
        if name[len(name)-1] == ' ' or name[len(name)-1] == '.':
            name = name[:len(name)-1]
        #check if actual name
        
        else:
            #finally check if in list already and if not add
            if name.find('\\') != -1:
                name = name[:name.find('\\')]
            parts = name.split()
            newName = parts[1] + " " + parts[2]
            if newName not in listOfNames:
                listOfNames.append(newName)

#load pickled captions
captions = pickle.load(open("save.p","rb"))

#filter out captions longer than 250 characters
for caption in captions:
    if len(caption) >= 250:
        captions.remove(caption)

#seperate captions into names based on punctuations and titles
listOfNames = []
names = []
for caption in captions:
    names = re.split(', |and |Ms. |Mrs. |Mr. |daughter |son |mother |father |sister |brother |wife |husband ', caption)
    i = 1
    for name in names:
        if len(name.split()) < 2:
            addName(name + ' ' + names[i-2])
        if len(name.split()) == 2:
            addName(name)
        if len(name.split()) == 3:
            addLargeName(name)
        i = i + 1

print(len(listOfNames))