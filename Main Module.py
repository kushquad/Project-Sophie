import os
import sys
import natlink
import time
import datetime
    
#Helper Functions
def speak(str):
    natlink.execScript('TTSPlayString "%s"'%str)
    print "Sophie>>",str

def search(str1,str2):
    return not str1.find(str2)==-1

def getUserInput():
    print ">>",
    return raw_input().lower()

def getGreeting():
    localhour = time.localtime(time.time()).tm_hour
    str = ""
    if(localhour>=5 and localhour<=11):
        str = "Good morning sir. I trust you are doing fine?"
    elif(localhour>=12 and localhour<=16):
        str = "Good afternoon sir. I trust you are doing great?"
    elif(localhour>=17 and localhour<=21):
        str = "Good evening sir. How are you doing?"
    else:
        str = "Quite late today sir. I hope you are doing fine?"
    return str

#Placeholder Modules
def callMusicModule():
    speak("Listing Music")
    print "Music List"
    print "----------"
    print ""
    count = 1
    for file in os.listdir("C:\\Users\\Kushagra\\Music"):
        if(
            os.path.isfile(os.path.join("C:\\Users\\Kushagra\\Music",file))
            and
            file.endswith(".mp3")
           ):
            print "%d."%count,file[:-4]
            count = count + 1
    print ""
    
#Initialisation
os.system("cls")
os.system("color 0b")
print "Loading Sophie v0.1 ",
natlink.natConnect()
for i in xrange(0,10):
    print '.',
    time.sleep(0.1)
print ' '
speak("Loading complete.")

#GREETING_STATE
speak(getGreeting())
p = getUserInput()
if(search(p,"fine") or search(p,"yes")):
    speak("I am pleased to hear that. How may I be of assistance?")
else:
    speak("I am sorry to hear about that. How may I help?")

#COMMAND_LOOP_STATE
while(1):
    p = getUserInput()
    if(p == "list music"):
        callMusicModule()
    elif(p == "exit"):
        break
    else:
        speak("I do not recognise that command yet.")

#Cleanup
natlink.natDisconnect()
print "Terminated."
