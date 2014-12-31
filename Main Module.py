import feedparser
import subprocess
import webbrowser
import traceback
import datetime
import urllib2
import natlink
import time
import sys
import os

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
def callTimeModule():
    curtime = time.localtime(time.time())
    speak("The current time is %d hours, %d minutes."
          %(curtime.tm_hour,curtime.tm_min))

def callYouTubeModule():
    speak("What video are you looking to watch?")
    searchstr = raw_input("Enter search string : ")
    keywordlis = searchstr.split(' ')
    keywordstr = '+'.join(keywordlis)
    webbrowser.open("www.youtube.com/results?search_query="+keywordstr)

def callGoogleModule():
    speak("What would you like to Google?")
    searchstr = raw_input("Enter search string : ")
    keywordlis = searchstr.split(' ')
    keywordstr = '+'.join(keywordlis)
    webbrowser.open("https://www.google.co.in/?gfe_rd=cr&ei=p0Sh\
                VI7WK6XM8geeioHAAg&gws_rd=ssl#q="+keywordstr)

def callBatteryModule():
    speak("Fetching battery status.")
    proc = subprocess.Popen('C:\\Users\\Kushagra\\Desktop\\Battery Test.exe',
                            stdout=subprocess.PIPE)
    data = proc.communicate()
    acstatus = int(data[0].split(' ')[0])
    batterylife = int(data[0].split(' ')[1])
    
    if(acstatus==0):
        speak("Deriving power from on-board battery.")
    else:
        speak("AC line power.")
    speak("Current battery percentage : %d percent."%batterylife)

def callMusicModule():
    speak("Listing Music")
    print ""
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

def callNoteWritingModule():
    speak("Creating a note. What would you like to name it?")
    filename = getUserInput()
    file = open("%sNOTE.txt"%filename,"w")
    speak("Have opened a note for you. Type ~ followed by enter to end note.")

    print ""
    print "%s.txt"%filename
    for i in xrange(0,len(filename)+4):
        sys.stdout.write('-')
    print ""

    text = ""
    while(text!="~"):
        text = raw_input()
        if(text!="~"):
            file.write(text)
            file.write('\n')
            
    file.close()
    speak("Have closed the note.")

def callAddApplicationModule():
    speak("Initiating application map service.")
    file = open("AppMap.txt",'r')
    speak("Populating list of registered applications.")
    count = 1
    print "S.no","Application Keyword"
    for line in file:
        details = line.split(' ')
        print "%d."%count, details[0]
    speak("Listing complete.")
    file.close()
    speak("Please key in the application path.")
    quitflag = False
    while(1):
        path = raw_input("Complete Path : ")
        if(os.path.isfile(path)):
            break
        elif path=="quit":
            quitflag = True
            break
        else:
            speak("Invalid file submitted for registration.")
    if(not quitflag):
        file = open("AppMap.txt",'a')
        speak("Enter keyword.")
        keyword = raw_input("Keyword : ")
        file.write(keyword+","+path)
        file.close()
        speak("Application has been successfully registered.")
    else:
        speak("Terminating application map service.")
        
def callApplicationModule(search):
    speak("Searching for registered application.")
    file = open("AppMap.txt",'r')
    for line in file:
        details = line.split(',')
        findflag = False
        if(details[0].lower()==search.lower()):
            findflag = True
            os.startfile(details[1],'open')
            speak("Application opened successfully")
            break
    if(not findflag):
        speak("Application keyword has not been registered.")
        
def callNoteReadingModule():
    speak("Accessing list of notes using set environment variables.")

    print ""
    print "Notes List"
    print "----------"
    print ""

    count = 1
    filenamelist = []
    for file in os.listdir("C:\\Users\\Kushagra\\Desktop"):
        if(
            os.path.isfile(os.path.join("C:\\Users\\Kushagra\\Desktop",file))
            and
            file.endswith("NOTE.txt")
           ):
            print "%d."%count,file[:-8]
            count = count + 1
            filenamelist.append(os.path.join("C:\\Users\\Kushagra\\Desktop",file))

    speak("Type the note names to access. Type exit to discontinue.")
    while(1):
        filename = getUserInput()
        if(filename=="exit"):
            speak("Note reading service discontinued. ")
            break
        flag = False
        filename = os.path.join("C:\\Users\\Kushagra\\Desktop",
                                "%sNOTE.txt"%filename)
        for filenametarg in filenamelist:
            if(filename==filenametarg):
                flag = True
                speak("Opening note.")
                f = open(filenametarg,"r")
                for line in f:
                    print line,
                f.close()
                break
        if(not flag):
            speak("No note of the given name exists!")
    
def callFacebookNotificationsModule():
    speak("Accessing Facebook notifications.")
    urlread = urllib2.urlopen(
        'https://www.facebook.com/feeds/notifications.php?id=100002762352191&viewer=100002762352191&key=AWj7hLrGf8xmfSJR&format=rss20')
    parsedurl = feedparser.parse(urlread)
    notifs = []
    speak("Notification read complete.")
    for i in range(len(parsedurl.entries)):
        notifs.append(parsedurl.entries[i].title)
    speak("Listing 5 recent notifications.")
    count = 1
    for i in notifs[:5]:
        print "%d."%count,i.encode('ascii','ignore')
        count = count + 1
    speak("Listing complete.")

    
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
try:
    while(1):
        p = getUserInput()
        if(p == "list music"):
            callMusicModule()
        elif(p == "write note"):
            callNoteWritingModule()
        elif(p == "read note" or p == "read notes"):
            callNoteReadingModule()
        elif(p == "get facebook notifications" or p == "get fb notifications"
             or p == "get facebook notifs" or p == "get fb notifs"):
            callFacebookNotificationsModule()
        elif(p == "get time"):
            callTimeModule()
        elif(p == "get battery"):
            callBatteryModule()
        elif(p == "google" or p == "search google"):
            callGoogleModule()
        elif(p == "youtube" or p == "search youtube"):
            callYouTubeModule()
        elif(p == "add app" or p == "add application"):
            callAddApplicationModule()
        elif(p.split(' ')[0]=="open" and len(p.split(' '))==2):
            callApplicationModule(p.split(' ')[1])
        elif(p == "kill power"):
            break
        else:
            speak("I do not recognise that command yet.")
except:
    print traceback.format_exc()
    speak("Something seems to have gone wrong. Kindly restart.")

#Cleanup
speak("Goodbye sir.")
natlink.natDisconnect()
print "Terminated."
