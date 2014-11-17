#Frequency Distribution Technique
    
responsefrequencytable = {"":{"":0}}

def simulatetraining():
    trainingset = open("QueryResponseTrainingSet2.txt",'r')
    count = 0
    for line in trainingset:
        count += 1
        if(count%3==1):
            prompt = line 
        elif(count%3==2):
            response = line
        else:
            train(prompt, response)

def tokenize(string):
    ''' Splits cleaned input string only by spaces for now, also excess
        spaces are removed.'''
    
    initlist = string.split(' ')
    finlist = []
    for token in initlist:
        if(not token==''):
            finlist.append(token.lower())
    return finlist

def clean(string):
    ''' For now we consider that words may be typed only using alphabets,
        lower or upper. Any special symbols or numbers are omitted, which of
        course means elimination of contraction forms of words'''

    l = len(string)
    tempstr = ""
    for i in xrange(0,l):
        if(
            (string[i]>='a' and string[i]<='z')
            or
            (string[i]>='A' and string[i]<='Z')
            or
            (string[i]==' ')
        ):
            tempstr += string[i]
        else:
            tempstr += ' '
    return tempstr

#Contraction replacer function must be before the clean function to convert
#contracted forms into proper words.

#After contraction replacement, cleaning and tokenizing, we may consider two
#approaches, an equalized word contribution approach by frequency distribution
#or grammar allocation.

#Training session until exit is entered
#Prompt and response are given as strings
def train(prompt,response):
    promptlist = tokenize(clean(prompt))
    response = response.rstrip()
    l = len(promptlist)
    for word in promptlist:
        if(word in responsefrequencytable):
            if(response in responsefrequencytable[word]):
                responsefrequencytable[word][response]+=1.0/l
            else:
                responsefrequencytable[word][response]=1.0/l
                #dict(
                #responsefrequencytable[word].items()+{response:1.0/l}.items())
        else:
                responsefrequencytable[word] = {response:1.0/l}
                
def fetchResponse(prompt):
    promptlist = tokenize(clean(prompt))
    cfd = {"":{"":0}}
    cfdsums = {}
    responselist = []
    for word in promptlist:
        probsum = 0
        if word not in responsefrequencytable:
            responsefrequencytable[word] = {"":0}
        for response in responsefrequencytable[word]:
            val = responsefrequencytable[word][response]
            probsum += responsefrequencytable[word][response]
            responselist.append(response)
            if(not response=="" and response in cfd):
                cfd[response][word] = val
                #dict(cfd[response].items()+{word:val}.items())
            else:
                cfd[response] = {word:val}
        cfdsums[word] = probsum
            
    responselist = list(set(responselist))
    responsedict = {}
    
    for response in responselist:
        responsevaluetemp = 0
        for word in cfd[response]:
            val = cfd[response][word]
            if(not cfdsums[word]==0):
                responsevaluetemp += val/cfdsums[word]
        responsedict[response] = responsevaluetemp

    maxval = -1
    tempstring = ""
    for response in responsedict:
        if(responsedict[response]>maxval):
            maxval = responsedict[response]
            tempstring = response

    #print cfd
    #print cfdsums
    #print responselist
    #print responsedict
    
    if(tempstring==""):
        return "I have no response to that."
    else:
        return tempstring
    

simulatetraining()
#print responsefrequencytable
flag = False
istrainingmode = False
while(not flag):
    if(istrainingmode):
        print "Train >> ",
        prompt = raw_input()
        if(prompt=="train"):
            istrainingmode = True
            continue
        if(prompt=="test"):
            istrainingmode = False
            continue
        if(prompt=="exit"):
            break
        print "Response >> ",
        response = raw_input()
        train(prompt,response)
        print responsefrequencytable
    else:
        print "Query >> ",
        prompt = raw_input()
        if(prompt=="train"):
            istrainingmode = True
            continue
        if(prompt=="test"):
            istrainingmode = False
            continue
        if(prompt=="exit"):
            break
        print "Sophie >> ",
        print fetchResponse(prompt)
