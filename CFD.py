#Frequency Distribution Technique
    
responsefrequencytable = {"":{"":0}}

def tokenize(string):
    ''' Splits cleaned input string only by spaces for now, also excess
        spaces are removed.'''
    
    initlist = string.split(' ')
    finlist = []
    for token in initlist:
        if(not token==''):
            finlist.append(token)
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
    l = len(promptlist)
    for word in promptlist:
        try:
            responsefrequencytable[word][response]+=1.0/l
        except KeyError:
                responsefrequencytable[word] = {response:0}
                
def fetchResponse(prompt):
    promptlist = tokenize(clean(prompt))
    cfd = {"":{"":0}}
    cfdsums = {}
    responselist = []
    for word in promptlist:
        probsum = 0
        for response in responsefrequencytable[word]:
            val = responsefrequencytable[word][response]
            probsum += responsefrequencytable[word][response]
            responselist.append(response)
            cfd[response] = {word:val}
        cfdsums[word] = probsum

    responselist = list(set(responselist))
    responsevalues = []
    for response in responselist:
        responsevaluetemp = 0
        for word in cfd[response]:
            val = cfd[response][word]
            responsevaluetemp += cfdsums[word]*val
        responsevalues.append(responsevaluetemp)

    maxi = -1
    idx = 0
    for i in xrange(0,len(responsevalues)):
        if(responsevalues[i]>maxi):
            maxi = responsevalues[i]
            idx = i
    return responselist[i]

flag = False
istrainingmode = True
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
        print fetchResponse(prompt)
